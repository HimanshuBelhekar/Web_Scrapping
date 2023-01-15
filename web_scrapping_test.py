from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://www.amazon.in/s?k=gaming+laptop&i=computers&sprefix=gaming%2Ccomputers%2C286&ref=nb_sb_ss_ts-doa-p_5_6"

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)

#print(webpage.content)

soup = BeautifulSoup(webpage.content, "html.parser")

#print(soup.prettify())

# title = soup.find_all("span", attrs={"class":'a-size-medium a-color-base a-text-normal'})

# print(title[0].text)

# price = soup.find_all("span", attrs={"class":'a-price-whole'})

# print(price[0].text)

# ratings = soup.find_all("span", attrs={"class":'a-icon-alt'})

# print(ratings[0].text)

#print("Price: " + soup.find("span", attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={"class":'a-price-whole'}).text)

#print("Rating: " + soup.find("span", attrs={"class":'a-icon-alt'}).text.strip())

links = soup.find_all("a", attrs={"class":'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

#print(links[0])

new_URL = "https://www.amazon.in" + links[0].get('href')

new_webpage = requests.get(new_URL, headers=HEADERS)

new_soup = BeautifulSoup(new_webpage.content, "html.parser")

#print(new_soup.prettify())

print("Title: " + new_soup.find("span", attrs={"id":'productTitle'}).text.strip())

print("Price: " + new_soup.find("span", attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={"class":'a-price-whole'}).text)

print("Rating: " + new_soup.find("span", attrs={"class":'a-icon-alt'}).text.strip())

print("Review: " + new_soup.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip())
