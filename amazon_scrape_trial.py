from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime


if __name__ == '__main__':

	#URL of website you want to scrape
	URL = "https://www.amazon.in/s?k=gaming+laptop&i=computers&sprefix=gaming%2Ccomputers%2C286&ref=nb_sb_ss_ts-doa-p_5_6"

	#Add your user agent. If not sure you can whatismybrowser website
	HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

	#HTTP request
	webpage = requests.get(URL, headers=HEADERS)

	#Soup object containing all the data from the website
	soup = BeautifulSoup(webpage.content, "html.parser")

	data = {"Title":[], "Price":[], "Rating":[]}

	title_list = soup.find_all("span", attrs={"class":'a-size-medium a-color-base a-text-normal'})

	price_list = soup.find_all("span", attrs={"class":'a-price-whole'})

	rating_list = soup.find_all("span", attrs={"class":'a-icon-alt'})

	#Function calls to get product information
	
	for title in title_list:
		data['Title'].append(title.text)


	for price in price_list:
		data['Price'].append(price.text)

	for rating in rating_list:
		data['Rating'].append(rating.text)

	# print(data)

	amazon_df = pd.DataFrame({ key:pd.Series(value) for key,value in data.items() })
	amazon_df['Title'].replace('', np.nan, inplace=True)
	amazon_df = amazon_df.dropna(subset=['Title'])
	amazon_df.to_csv("Amazon_data" + datetime.now().strftime("_%d_%m_%Y_%H_%M_%S") + ".csv", header=True, index=False)

	print(amazon_df)