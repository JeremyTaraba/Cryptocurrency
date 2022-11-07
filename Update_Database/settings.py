TOTAL_COINS = 100   # max is 250
TOTAL_TWEETS = 100 # max is 900 per 15 minutes 

# 2 runs for updating the database (24hrs apart for 24 hour predictions)
# First run at 7PM 11/5 over 100 coins and 100 tweets
# Second run at 7PM 11/6

# Takes about an hour to update the database, most of the time is taken calculating polarity for the tweets
# polarity isnt even that needed. research shows it rarely helps and may even hurt the model. Amount of 
# google searches in last day is more accurate or something like that 

# potential problem with running 24 hours apart is that the order of coins may change since it is ordered based on rank
# this would mess up the model since we don't check names when putting the data together