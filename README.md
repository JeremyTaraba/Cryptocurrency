## Cryptocurrency Machine Learning Predictor

## Introduction

In this era of gradual web 3.0 and decentralization, more and more virtual currencies appear in today's market. Bitcoin, as the largest virtual currency, has the advantages of market consensus and other advantages. The most important thing is that Bitcoin has a network effect as a currency, and the Bitcoin network can also evolve, while other virtual currencies themselves are not sufficiently decentralized. However, due to the two shortcomings of Bitcoin, that is, the first mining period has long passed and no coins can be mined, and many national policies do not support it, so the risk of mining coins is relatively high. Many people will look at other virtual currencies in the market, hoping to achieve a huge profit. However, the currencies in the market are mixed, and many speculators do not have professional knowledge about blockchain and various virtual currencies. As a result, many people will take great risks when purchasing virtual currencies, and may even go bankrupt. So, we want to make this project to help people who want to buy virtual currency but don't have the time or energy to research it. They can use my app to clearly see the various data of each virtual currency in the market and the market's evaluation of this virtual currency. We will also use this information to score and rank these virtual currencies using regression algorithms.


### Purpose 
This program showcases the effectiveness of using machine learning to predict future cryptocurrency price changes. It will show how accurate or inaccurate using a regression algorithm with specific data from each coin is for predicting a 24 hour price change.


### Method
Before we can predict anything we first need to get some data. Our data is gathered from coinGecko.com's API and then stored in a database hosted by firebase. The tweets are gathered using twitter's API and Postman.com to connect it with python code. The tweets are cleaned of stop words and punctuation using nltk and the polarity is calculated using textblob. Once all the data is gathered we can use a Forest Regressor Algorithm from sklearn to split our data and then train a model. This model is then given new data make its prediction.


### Details

There are two big components for this project. One of them is using APIs to first get information about our cryptocurrencies and also to get tweets for each crypto. The second big component is our regression algorithm used to process the data. Also the amount of cryptocurrencies and data for each currency is too massive to practically be stored locally and so a cloud database is required. Currently we have the top 100 coins and 100 tweets for each coin used to calculate the polarity. 

The tweets were processed to clean them of usernames, hyperlinks, and punctuation using regex expressions and then cleaned of stop words using a Python library called NLTK. A Porter stemming algorithm from the NLTK library was then used to stem each word in the tweets. All of this was necessary to efficiently implement a sentiment analysis algorithm from the Python library TextBlob. This algorithm analyzed the tweets and returned a polarity score based on the content of the tweet. This data was used to help the machine learning algorithm accurately predict the price change of each coin. 

The machine learning algorithm uses a machine learning library for Python called Scikit-learn. Scikit-learn has many algorithms including prediction algorithms like Random Forest Regression which is used in the program to predict the price change of each coin. Random Forest Regression splits the data into binary trees which are then traversed randomly in order to make a prediction. The predictions from each of the trees are then averaged and used to make a more accurate prediction. To train the Random Forest Regression algorithm, a class called train test split from Scikit-learn is used to quickly split the data from the database into training and testing sets. This allows the algorithm to be trained using the training set and then tested using the test set to see how well the model performed. Before importing the data, a Python library called Pandas is used to manipulate the data for each coin into a dataframe so splitting the data into train and test sets is efficient. An R2 score is used from the Scikit-learn library to calculate how well the model performed. The R2 score compares the test data results with the actual results and returns a number. If the number returned is close to one then the model performed well but if the number is far away from one then the model performed poorly. The algorithm is trained until a score close to one is achieved. This trained algorithm is then used to predict the future price change of each coin.



### Results





### Similar Works

#### Related Work 1
https://www.researchgate.net/profile/Bhanu-Kolla/publication/344151224_Predicting_Crypto_Currency_Prices_Using_Machine_Learning_and_Deep_Learning_Techniques/links/5f55c995299bf13a31a7c9ed/Predicting-Crypto-Currency-Prices-Using-Machine-Learning-and-Deep-Learning-Techniques.pdf


This work explores different machine learning algorithms such as Linear Regression models with different features and Recurrent Neural Networks and it compares each one. The goal is to show that the price of Bitcoin can be accurately predicted using machine learning, which they successfully prove. Compared to my work, this work uses two different algorithms and only tries to use the model to predict the price of Bitcoin over a period of time. My work tries to predict the future price of Bitcoin and uses an ensemble regression model. This work strictly uses previous data from Bitcoin to train the model and does not use sentiment analysis which shows the strength of their model to be so accurate with only historical prices.


#### Related Work 2

http://103.47.12.35/bitstream/handle/1/9794/bt3309.pdf?sequence=1&isAllowed=y


This paper [3] proposes three different types of recurrent neural network models to predict the prices of three different crypto currencies. The gated recurrent unit performed better than long short term memory and bidirectional long short term memory when comparing accuracy. Compared to my work, this paper compares three different models and only tests it on three different coins. It also examines Random Forest Regressor and uses an 80% training set and 20% test set while I used a 70% training set and 30% test set. The strength of this is having trained with more information. This paper also brings up the economical problems of having an algorithm that can accurately predict the price of cryptocurrencies and stocks.


#### Related Work 3
https://scholar.smu.edu/cgi/viewcontent.cgi?article=1039&context=datasciencereview



This paper attempts to find a solution to predicting cryptocurrency price changes using sentiment analysis of tweets. They concluded that sentiment analysis for prediction is not as effective when the price is falling but instead Google trends and tweet volume are much better for prediction. Compared to my work, this paper uses a Python Twitter library called Tweepy for Python API called while I used Postman to call the Twitter API. Both approaches effectively tweets from Twitter. This paper cleans the tweets similarly to how I cleaned my tweets before using a sentiment analysis algorithm. This paper does not use machine learning but instead only uses the polarity of the tweets to tell if the cryptocurrency will increase or decrease.







