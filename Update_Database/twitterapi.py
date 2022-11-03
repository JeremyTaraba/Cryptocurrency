from functools import total_ordering
import requests
import json
import re
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob
import settings


payload={}
headers = {
  'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAJtbgwEAAAAAEAieskSy%2FW9LFVVj%2BuUeW39%2FRMU%3DyavmJg7HfhZQYKCViV23zQnnjtn2C1VKUtl7daHFfBHGvzqRcC',
  'Cookie': 'guest_id=v1%3A166319300522636822'
}



def cleanName(name):
    name = re.sub(r"[^a-zA-Z0-9 ]"," ", name)
    return name



def cleanText(text):
    text = text.lower()
    # Removes all mentions (@username) from the tweet since it is of no use to us
    text = re.sub("@[A-Za-z0-9_]+","", text)
    text = re.sub("#[A-Za-z0-9_]+","", text)

    # Removes any link in the text
    text = re.sub('http://\S+|https://\S+', '', text)
    text = re.sub(r"www.\S+", "", text)

    # Only considers the part of the string with char between a to z or digits and whitespace characters
    # Basically removes punctuation
    text = re.sub('[()!?]', ' ', text)
    text = re.sub('\[.*?\]',' ', text)
    # filter out alphanumeric characters
    text = re.sub("[^a-z0-9]"," ", text)

    # Removes stop words that have no use in sentiment analysis 
    text_tokens = word_tokenize(text) # break string into singular words
    text = [word for word in text_tokens if not word in stopwords.words()]

    text = ' '.join(text) # join the list together in a string
    return text




def stem(text):
  # This function is used to stem the given sentence
  porter = PorterStemmer()
  token_words = word_tokenize(text)
  stem_sentence = []
  for word in token_words:
    stem_sentence.append(porter.stem(word))
  return " ".join(stem_sentence)




def sentiment_polarity(cleaned_text):
  # Returns the sentiment based on the polarity of the input TextBlob object
  text = TextBlob(cleaned_text)
  return text.sentiment.polarity
    


def calculate_polarity(tweets):
  totalPolarity = 0
  for i in tweets:
    totalPolarity = sentiment_polarity(i) + totalPolarity

  # if(totalPolarity > 1):
  #   totalPolarity = 1
  # if(totalPolarity < -1):
  #   totalPolarity = -1

  return totalPolarity

  

def getcointweets(coin_name):
    coin_name = cleanName(coin_name)
    url = "https://api.twitter.com/2/tweets/search/recent?query="+str(coin_name)+" -is:retweet&max_results="+str(settings.TOTAL_TWEETS)+"&user.fields=verified"
    tweets = []
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    #print(data)
    #print(coin_name)
    for i in data["data"]:
        text = cleanText(i["text"])
        text = stem(text)
        tweets.append(text)
    
    return tweets

#getcointweets("bitcoin")

