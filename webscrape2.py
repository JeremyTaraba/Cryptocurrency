import requests
from bs4 import BeautifulSoup

  
URL = "https://www.reddit.com/r/CryptoCurrency/"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
#print(soup.prettify()) # to see what the html looks like
quotes=[]  # a list to store quotes

div = soup.find('div', atrs={"data-adclicklocation":"title"})
title = div.find('h3', attrs={"class":"_eYtD2XCVieq6emjKBH3m"})
print(title)

# table = soup.find('div', attrs = {'id':'all_quotes'})  

# #print(table.prettify()) # to see what our table is doing
   


# for row in table.findAll('div', attrs = {'class':'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'}):
#     quote = ""
#     quote = row.img['alt'].split(' #')[0]
#     quotes.append(quote)
   

# file1 = open("inspirational_quotes.txt", "w")
# for i in quotes:
#     file1.write(i)
#     file1.write("\n")