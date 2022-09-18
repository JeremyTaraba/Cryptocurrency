import re
import time
from sched import scheduler
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
import pause
import requests
import tweepy
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import json
import firebase_admin
from firebase_admin import db
import datetime as dt

import lxml
from firebase_admin import credentials, firestore

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from pandas.core.frame import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor

# Retrospect Server File to fetch data and analyze

# ---------------------------------------------------------------------------------------------------
# Definitions til line 149, keep scrolling boys
cred = credentials.Certificate(r"Firebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crypto-project-001-default-rtdb.firebaseio.com'
})
dbFirestore = firestore.client()

my_api_key = "KsuOmLym8qJQLcvdC3kKggMS5"
my_api_secret = "uqFemcDE9T5xqxxYdaIK8fFn9UEdsxyp7DoTgTTdexLrPLkCkN"
my_access_token = "1424002307717570564-K60SfTLZxpMDwjWZQLrqS4QQiVHRi5"
my_access_secret = "j17ICE8oBmlKPvDN6R1JbtjabyX0YEsQxmuVOQgEK9YG2"

client = tweepy.Client(consumer_key=my_api_key, consumer_secret=my_api_secret, access_token=my_access_secret,
                       access_token_secret=my_access_secret,
                       bearer_token="AAAAAAAAAAAAAAAAAAAAAOlkdwEAAAAAQPK9bzwm2oIPQL1mcVVrvn7dP4Q%3Df61vnOIToXEHbBoXP76eVAVtDdqH4YPMQK1FDraK521GF6o67i")

my_api_key2 = "6pH0p4Tt3tAMylIsX0HWt1CiL"
my_api_secret2 = "yodtkh0LuDmGiNFvDIrNjH8iwT9kcm8Z6OvncMY52qNYFzf7m0"
my_access_token2 = "1557071731663294464-pQWtnOEWERGnb6M1cOwhQjCIQsHyqH"
my_access_secret2 = "34ukhv9kURso8q60PbfQWJykAHeyAgueSMT4R0dPjUCfu"

client2 = tweepy.Client(consumer_key=my_api_key2, consumer_secret=my_api_secret2, access_token=my_access_secret2,
                        access_token_secret=my_access_secret2,
                        bearer_token="AAAAAAAAAAAAAAAAAAAAAIAnfwEAAAAA9ou4xSwxWQS4snMw5LLzVTiuRD4%3Dg2rXFxm850aEvS7AlRryeySeZRlvCGzK7UVdVrjOhPaJjnzW2c")

stop_words = nltk.corpus.stopwords.words(['english'])

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4')

lem = WordNetLemmatizer()

def cleaning(data):
    # remove urls
    tweet_without_url = re.sub(r'http\S+', ' ', data)

    # remove hashtags
    tweet_without_hashtag = re.sub(r'#\w+', ' ', tweet_without_url)

    # 3. Remove mentions and characters that not in the English alphabets
    tweet_without_mentions = re.sub(r'@\w+', ' ', tweet_without_hashtag)
    precleaned_tweet = re.sub('[^A-Za-z]+', ' ', tweet_without_mentions)

    # 2. Tokenize
    tweet_tokens = TweetTokenizer().tokenize(precleaned_tweet)

    # 3. Remove Puncs
    tokens_without_punc = [w for w in tweet_tokens if w.isalnum()]

    # 4. Removing Stopwords
    tokens_without_sw = [t for t in tokens_without_punc if t not in stop_words]

    # 5. lemma
    text_cleaned = [lem.lemmatize(t) for t in tokens_without_sw]

    # 6. Joining
    return " ".join(text_cleaned)

def clean_tweets(tweets):
    cleaned_tweets = []
    if (tweets is None):
        # print("what")
        return cleaned_tweets
    for i in range(len(tweets)):
        if tweets[i] is not None:
            cleaned_tweets.append(cleaning(str(tweets[i])))
        else:
            cleaned_tweets.append("")
    # for tweet in tweets:
    #     cleaned_tweets.append(cleaning(str(tweet)))
    return cleaned_tweets

def get_polarity(tweet):
    polarity = TextBlob(tweet).sentiment.polarity
    # scale of subjectivity or objectivity
    # -: neg, +: positive
    # When a sentence is passed into Textblob it gives two outputs, which are polarity and subjectivity.
    # Polarity is the output that lies between [-1,1], where -1 refers to negative sentiment and +1 refers to positive sentiment.
    return polarity

def set_data(collect: str, data: dict):
    ref = db.reference(f'database/{collect}')  # opens collection

    toRemove = []
    toAdd = []

    for key in data:
        newKey = key.replace('[','')
        newKey = newKey.replace(']', '')
        if newKey != key:
            toRemove.append(key)
            toAdd.append(newKey)

    for i in range(len(toRemove)):
        data[toAdd[i]] = data[toRemove[i]]
        del data[toRemove[i]]

    ref.set(data)
    # for name in documents:
    #     # print("Processing", name['id'])
    #     doc = collection.document(documents[name]['id'])  # specifies the  document
    #     # print(data[name])
    #     if name in data:
    #         doc.set(data[name])
    #     # print(data[name['id']])

def update_data(collect: str, data: dict):
    ref = db.reference(f'database/{collect}')  # opens collection

    toRemove = []
    toAdd = []

    for key in data:
        newKey = key.replace('[', '')
        newKey = newKey.replace(']', '')
        if newKey != key:
            toRemove.append(key)
            toAdd.append(newKey)

    for i in range(len(toRemove)):
        data[toAdd[i]] = data[toRemove[i]]
        del data[toRemove[i]]

    for name in data:
        crypto_ref = ref.child(name)
        for item in data[name]:
            crypto_ref.update({item: data[name][item]})

def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:
        #Over midnight:
        return nowTime >= startTime or nowTime <= endTime

keepers = ['score', 'prediction', 'marketView']


def save_history(collect: str, data: dict):
    ref = db.reference(f'history/{collect}')  # opens collection


    toRemove = []
    toAdd = []

    for key in data:
        newKey = key.replace('[','')
        newKey = newKey.replace(']', '')
        if newKey != key:
            toRemove.append(key)
            toAdd.append(newKey)

    for i in range(len(toRemove)):
        data[toAdd[i]] = data[toRemove[i]]
        del data[toRemove[i]]

    now = int(time.time())

    for name in data:
        crypto_ref = ref.child(f'{name}/{now}')
        crypto_ref.set(data[name])

# ---------------------------------------------------------------------------------------------------

app = Flask(__name__)

def updatePriceData():
    TopCryptos = {}
    excludedItems = ['fully_diluted_valuation', 'market_cap_change_24h', 'atl', 'atl_change_percentage', 'atl_date',
                     'roi']

    with open('target_cryptos.json') as json_file:
        TopCryptos = json.load(json_file)

    adding = []
    adding.append("")
    idx = 0
    count = 0

    for crypto in TopCryptos:
        if count == 50:
            count = 0
            idx += 1
            adding.append("")
        if count != 0:
            adding[idx] += ","
        adding[idx] += crypto
        count += 1

    for i in range(len(adding)):
        # print(i)
        response = requests.get(
            f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={adding[i]}&order=market_cap_desc&per_page=100&page=1&sparkline=false')
        # print(response.json())
        for res in response.json():
            TopCryptos[res['id']]['id'] = res['id']
            for item in res:
                if item not in excludedItems:
                    # Filter data and only keep what we need
                    TopCryptos[res['id']][item] = res[item]

    set_data("cryptos", TopCryptos)

def cryptoDataFetch():
    # define variables
    TopCryptos = {}
    # CryptosList = {}
    CryptosCommit = {}
    CryptosTweets = {}

    # code settings
    doWholeGithubAPI = 1  # 0: dont wait for whole API; 1: do whole API
    doWholeTwitterAPI = 1  # 0: dont wait for whole API; 1: do whole API
    skipGithubAPI = 0  # 0: dont skip; 1: skip
    skipTwitterAPI = 0  # 0: dont skip; 1: skip
    doOnlyFirst50 = 0  # 0: do 1000; 1: only first 50
    skipGetSource = 0  # 0: scrape; 1: skip
    numberOfCryptos = 500
    excludedItems = ['fully_diluted_valuation', 'market_cap_change_24h', 'atl', 'atl_change_percentage', 'atl_date',
                     'roi']

    with open('target_cryptos.json') as json_file:
        TopCryptos = json.load(json_file)

    # CryptosList = TopCryptos.copy()

    adding = []
    adding.append("")
    idx = 0
    count = 0

    for crypto in TopCryptos:
        if count == 50:
            count = 0
            idx += 1
            adding.append("")
        if count != 0:
            adding[idx] += ","
        adding[idx] += crypto
        count += 1

    for i in range(len(adding)):
        # print(i)
        response = requests.get(
            f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={adding[i]}&order=market_cap_desc&per_page=100&page=1&sparkline=false')
        # print(response.json())
        for res in response.json():
            TopCryptos[res['id']]['id'] = res['id']
            for item in res:
                if item not in excludedItems:
                    # Filter data and only keep what we need
                    TopCryptos[res['id']][item] = res[item]

    set_data('cryptos', TopCryptos)

    if skipGithubAPI == 0:
        idx = -1;

        # print("Github API")
        for source in TopCryptos:
            idx += 1
            if TopCryptos[source]['source'].find('github') == -1:
                if idx < len(TopCryptos):
                    CryptosCommit[source] = {'none': 'couldnt get'}
                continue

            if len(TopCryptos[source]['source'].split('/')) < 5:
                # Get most favorited repo
                r = requests.get(TopCryptos[source]['source'])
                soup = BeautifulSoup(r.content, 'lxml')

                table = soup.find('div', attrs={'class': 'org-repos repo-list'})

                if table is None:
                    if (idx < len(TopCryptos)):
                        CryptosCommit[source] = {'none': 'couldnt get'}
                    else:
                        break
                    continue
                max = 0
                repo = ""

                for row in table.find_all('li', attrs={'class': 'Box-row'}):
                    fav = row.find('svg', attrs={'class': 'octicon octicon-star mr-1'})
                    link = fav.parent

                    nOfFavs = int(re.sub(r"[\n\t\s]*", "", str(link).split('</svg>')[1].split('<')[0]).replace(',', ""))

                    if nOfFavs > max:
                        repo = row.div.div.div.a['href'].split('/')[2]
                        max = nOfFavs
            else:
                repo = TopCryptos[source]['source'].split('/')[4]

            URL = f"https://api.github.com/repos/{TopCryptos[source]['source'].split('/')[3]}/{repo}/stats/commit_activity"

            headers = {
                "accept": "application/vnd.github.v3+json"
            }

            r = requests.get(URL, headers=headers, auth=('bx07', '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'))

            if r.status_code != 200:
                if doWholeGithubAPI == 1:
                    if r.status_code == 403:
                        r = requests.get('https://api.github.com/rate_limit', headers=headers,
                                         auth=('bx07', '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'))
                        pause.until(int(r.json()['resources']['core']['reset']))

                        r = requests.get(URL, headers=headers)
                        if r.status_code != 200:
                            CryptosCommit[TopCryptos[idx]['id']] = {'none': 'couldnt get'}
                            continue
                    else:
                        continue
                else:
                    if (idx < len(TopCryptos)):
                        CryptosCommit[source] = {'none': 'couldnt get'}
                    else:
                        break
                    continue

            result = r.json()
            lastRow = result[len(result) - 1]
            prevRow = result[len(result) - 2]
            CryptosCommit[source] = {}
            if (idx < len(TopCryptos)):
                CryptosCommit[source]['0'] = prevRow
                CryptosCommit[source]['1'] = lastRow
            else:
                break

        set_data("commits", CryptosCommit)

    x = dt.datetime.now()
    limit = int(x.strftime('%H'))


    if skipTwitterAPI == 0:
        for crypto in TopCryptos:
            query = str(crypto)

            try:
                tweets = client.get_recent_tweets_count(query=query)
            except tweepy.errors.TooManyRequests:
                try:
                    tweets = client2.get_recent_tweets_count(query=query)
                except tweepy.errors.TooManyRequests:
                    if doWholeTwitterAPI == 1:
                        time.sleep(960)
                        try:
                            tweets = client.get_recent_tweets_count(query=query)
                        except tweepy.errors.TooManyRequests:
                            print("failed twice, API stopped")
                            CryptosTweets[crypto] = {'none': 'couldnt get'}
                            break;
                except:
                    print("Something else went wrong!")
                    CryptosTweets[crypto] = {'none': 'couldnt get'}
                    continue
            except:
                print("Something else went wrong!")
                CryptosTweets[crypto] = {'none': 'couldnt get'}
                continue

            tweetsCount = {}

            if tweets is None:
                CryptosTweets[crypto] = {'none': 'couldnt get'}

            for line in tweets[0]:
                date = line['start'].split('T')[0]
                thisTime = line['start'].split('T')[1].split(':')[0]

                if int(thisTime) > limit:
                    # only keep the counts to that hour so in the morning numbers dont look whack af
                    continue

                if date in tweetsCount:
                    tweetsCount[date] = tweetsCount[date] + int(line['tweet_count'])
                else:
                    tweetsCount[date] = int(line['tweet_count'])

            CryptosTweets[crypto] = tweetsCount

        set_data('tweets', CryptosTweets)

    # FINISHED CODE PART 1! DATA ANALYSIS PART:

    # Data analysis time
    # declare variables
    NewTopCryptos = []
    TopCryptosInfo = {}
    CryptosTweetsMessage = {}
    TweetsMarketview = {}
    TopCryptosChange = []
    CryptosPredictions = {}
    X = []
    # TweetCount = {}

    # settings
    readFromFirestore = 0
    doFirstNums = 0
    Nums = 15
    maxResults = 10
    doWholeAPI = 1
    writeInto = 1
    excludedItems = ['market_cap_rank', 'current_price', 'price_change_percentage_24h']

    counter = 0

    for cryptoName in TopCryptos:
        if doFirstNums == 1:
            if (counter > Nums):
                break
        NewTopCryptos.append(TopCryptos[cryptoName]['id'])
        TopCryptosInfo[cryptoName] = {}

        TopCryptosInfo[cryptoName]['marketCap'] = TopCryptos[cryptoName]['market_cap_rank']
        if TopCryptos[cryptoName]['market_cap_rank'] is None:
            TopCryptosInfo[cryptoName]['marketCap'] = 1000
        TopCryptosInfo[cryptoName]['price'] = TopCryptos[cryptoName]['current_price']
        if TopCryptos[cryptoName]['price_change_percentage_24h'] is not None:
            TopCryptosChange.append(int(TopCryptos[cryptoName]['price_change_percentage_24h'] * 100))
        else:
            TopCryptosChange.append(0)
        counter += 1

    counter = 0
    twMax = 100
    twMin = -50
    cmMax = 100
    cmMin = -50

    for cryptoName in CryptosTweets:
        if doFirstNums == 1:
            if (counter > Nums):
                break
        if not "none" in CryptosTweets[cryptoName]:
            TopCryptosInfo[cryptoName]['tweets'] = 0;
            idx = 0
            day0 = 0
            day7 = 0
            for date in CryptosTweets[cryptoName]:
                if idx == 0:
                    day0 = CryptosTweets[cryptoName][date]
                if idx == 7:
                    day7 = CryptosTweets[cryptoName][date]
                idx += 1

            if day0 != 0:
                TopCryptosInfo[cryptoName]['tweets'] = int((day7 - day0) / day0 * 100)
            else:
                TopCryptosInfo[cryptoName]['tweets'] = 100
            if TopCryptosInfo[cryptoName]['tweets'] > 0 and TopCryptosInfo[cryptoName]['tweets'] > twMax:
                twMax = TopCryptosInfo[cryptoName]['tweets']
            if TopCryptosInfo[cryptoName]['tweets'] < 0 and TopCryptosInfo[cryptoName]['tweets'] < twMin:
                twMin = TopCryptosInfo[cryptoName]['tweets']
        else:
            if not cryptoName in TopCryptosInfo:
                TopCryptosInfo[cryptoName] = {}
            TopCryptosInfo[cryptoName]['tweets'] = 0
        counter += 1

    counter = 0

    for cryptoName in CryptosCommit:
        if doFirstNums == 1:
            if (counter > Nums):
                break
        if not "none" in CryptosCommit[cryptoName]:
            TopCryptosInfo[cryptoName]['commits'] = 0

            week0 = 0
            week1 = 0

            for date in CryptosCommit[cryptoName]['0']['days']:
                week0 += int(date)
            for date in CryptosCommit[cryptoName]['1']['days']:
                week1 += int(date)

            if week0 != 0:
                TopCryptosInfo[cryptoName]['commits'] = int((week1 - week0) / week0 * 100)
            else:
                TopCryptosInfo[cryptoName]['commits'] = 100

            if TopCryptosInfo[cryptoName]['commits'] > 0 and TopCryptosInfo[cryptoName]['commits'] > cmMax:
                cmMax = TopCryptosInfo[cryptoName]['commits']
            if TopCryptosInfo[cryptoName]['commits'] < 0 and TopCryptosInfo[cryptoName]['commits'] < cmMin:
                cmMin = TopCryptosInfo[cryptoName]['commits']
        else:
            if not cryptoName in TopCryptosInfo:
                TopCryptosInfo[cryptoName] = {}
            TopCryptosInfo[cryptoName]['commits'] = 0
        counter += 1

    # ------------------------------------------------------------------------------
    # Process everything

    counter = 0

    for crypto in TopCryptos:
        if doFirstNums == 1:
            if (counter > Nums):
                break
        query = f'"{str(crypto)}" -is:retweet '
        tweets = None
        try:
            tweets = client.search_recent_tweets(query=query, max_results=maxResults)
        except Exception as e:
            try:
                tweets = client2.search_recent_tweets(query=query, max_results=maxResults)
            except Exception as e2:
                if (doWholeAPI == 1):
                    if (e.__class__.__name__ == "TooManyRequests"):
                        time.sleep(901)
                        try:
                            tweets = client.search_recent_tweets(query=query, max_results=maxResults)
                        except:
                            try:
                                tweets = client2.search_recent_tweets(query=query, max_results=maxResults)
                            except Exception as e2:
                                print("didnt work again.... Twitter fix!!!!!!!!!!!!!!!!!")
                    else:
                        tweets = None


        if tweets is not None:
            CryptosTweetsMessage[crypto] = clean_tweets(tweets.data)
        else:
            CryptosTweetsMessage[crypto] = []
        TweetsMarketview[crypto] = 0
        for tweet in CryptosTweetsMessage[crypto]:
            TweetsMarketview[crypto] += (get_polarity(tweet) * 100) / maxResults

        CryptosPredictions[crypto] = {}
        CryptosPredictions[crypto]['marketView'] = TweetsMarketview[crypto]

        CryptosPredictions[crypto]['commits'] = 0
        CryptosPredictions[crypto]['tweets'] = 0

        # print(crypto)
        data = [TopCryptosInfo[crypto]['marketCap'], TopCryptosInfo[crypto]['price'],
                CryptosPredictions[crypto]['marketView']]

        CryptosPredictions[crypto]['score'] = TweetsMarketview[crypto] * 0.5 + (
                    (501 - TopCryptosInfo[crypto]['marketCap']) / 5) * 0.02
        # continue from here
        if 'tweets' in TopCryptosInfo[crypto]:
            CryptosPredictions[crypto]['tweets'] = TopCryptosInfo[crypto]['tweets']
            data.append(TopCryptosInfo[crypto]['tweets'])
            if TopCryptosInfo[crypto]['tweets'] > 0:
                CryptosPredictions[crypto]['score'] += ((TopCryptosInfo[crypto]['tweets']) / twMax * 100) * 0.3
            if TopCryptosInfo[crypto]['tweets'] < 0:
                CryptosPredictions[crypto]['score'] += ((TopCryptosInfo[crypto]['tweets']) / twMin * -100) * 0.3

        else:
            data.append(0)

        if 'commits' in TopCryptosInfo[crypto]:
            data.append(TopCryptosInfo[crypto]['commits'])
            CryptosPredictions[crypto]['commits'] = TopCryptosInfo[crypto]['commits']
            if TopCryptosInfo[crypto]['commits'] > 0:
                CryptosPredictions[crypto]['score'] += ((TopCryptosInfo[crypto]['commits']) / cmMax * 100) * 0.22
            if TopCryptosInfo[crypto]['commits'] < 0:
                CryptosPredictions[crypto]['score'] += ((TopCryptosInfo[crypto]['commits']) / cmMin * -100) * 0.22
        else:
            data.append(0)

        X.append(data)
        counter += 1

    X_train, X_test, y_train, y_test = train_test_split(X, TopCryptosChange, test_size=0.7)

    regr = RandomForestRegressor()
    # fit data from previous sessions too!
    regr.fit(X_train, y_train)

    ML = dbFirestore.collection('ML').get()

    TestDataX = []
    TestDataY = []

    saveCount = 0

    for doc in ML:
        breakDown = []
        content = doc.to_dict()
        for data in content:
            breakDown.append(content[data])
        if 'X' in doc.id:
            TestDataX.append(breakDown)
            saveCount += 1
        else:
            TestDataY.append(breakDown)

    if (saveCount > 50):
        writeInto = 0

    for i in range(len(TestDataX)):
        regr.fit(TestDataX[i], TestDataY[i])

    if writeInto == 1:
        collection = dbFirestore.collection("ML")
        doc1 = collection.document('X' + str(time.time()))
        doc2 = collection.document('Y' + str(time.time()))

        data1 = {}
        data2 = {}

        for i in range(len(X_train)):
            data1[str(i)] = X_train[i]

        for i in range(len(y_train)):
            data2[str(i)] = y_train[i]

        doc1.set(data1)
        doc2.set(data2)

    # Save past data to improve model, then pass on firestore to the app
    # Machine learning works Boyyssssssssssssssssssss EZZZZZZZZ

    # And now......... we process every cryptooooooooooooooooooooooooooooooooooooooooooo

    iRange = 0
    counter = 0

    y_pred = regr.predict(X)

    for crypto in TopCryptos:
        CryptosPredictions[crypto]['prediction'] = str(int((y_pred[iRange])) / 100)

        # for item in TopCryptosInfo[crypto]:
        #     if item not in excludedItems:
        #         TopCryptos[crypto][item] = str(TopCryptosInfo[crypto][item])

        iRange += 1
        counter += 1

    set_data('predictions', CryptosPredictions)

    if isNowInTimePeriod(dt.time(23, 0), dt.time(0,0), dt.datetime.now().time()):
        save_history('main', CryptosPredictions)



scheduler = BackgroundScheduler()
scheduler.add_job(func=cryptoDataFetch, trigger="cron", minute='0', hour='*/1', day_of_week='*', week='*', month='*')
scheduler.add_job(func=updatePriceData, trigger="cron", minute='*/5', hour='*', day_of_week='*', week='*', month='*')
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def grabData():
    TopCryptos = []

    docs = db.reference('database/cryptos')
    data = docs.get()
    docs2 = db.reference('database/predictions')
    data2 = docs2.get()
    for key in data:
        newDict = data[key].update(data2[key])

        TopCryptos.append(data[key])

    # counter = 0
    # for doc in docs:
    #     # print(doc.to_dict())
    #     strDoc = json.dumps(doc.to_dict())
    #     # TopCryptos[doc.get('name')] = strDoc;
    #     TopCryptos.append(strDoc);
    #     counter += 1

    return jsonify(TopCryptos);


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
