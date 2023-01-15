from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime

#Function to get the Product Title
def get_title(soup):

	try:
		title = soup.find("span", attrs={"id":'productTitle'}).text.strip()

	except AttributeError:
		title = ""

	return title

#Function to get the Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={"class":'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).find("span", attrs={"class":'a-price-whole'}).text

	except AttributeError:
		price = ""

	return price


#Function to get the Product Rating
def get_rating(soup):

	try:
		rating = soup.find("span", attrs={"class":'a-icon-alt'}).text.strip()

	except AttributeError:
		rating = ""

	return rating

def get_review(soup):

	try:
		review = soup.find("span", attrs={"id":'acrCustomerReviewText'}).text.strip()

	except AttributeError:
		review = ""

	return review

if __name__ == '__main__':

	#URL of website you want to scrape
	URL = "https://www.amazon.in/s?k=gaming+laptop&i=computers&sprefix=gaming%2Ccomputers%2C286&ref=nb_sb_ss_ts-doa-p_5_6"

	#Add your user agent. If not sure you can whatismybrowser website
	HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

	#HTTP request
	webpage = requests.get(URL, headers=HEADERS)

	#Soup object containing all the data from the website
	soup = BeautifulSoup(webpage.content, "html.parser")

	#Fetch all the links
	links = soup.find_all("a", attrs={"class":'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

	links_list = []

	for link in links:
		links_list.append("https://www.amazon.in" + link.get('href'))

	#print(links_list)

	data = {"Title":[], "Price":[], "Rating":[], "Review":[]}

	for link in links_list:
		new_webpage = requests.get(link, headers=HEADERS)

		new_soup = BeautifulSoup(new_webpage.content, "html.parser")

		#Function calls to get product information
		data['Title'].append(get_title(new_soup))
		data['Price'].append(get_price(new_soup))
		data['Rating'].append(get_rating(new_soup))
		data['Review'].append(get_review(new_soup))

	#print(data)

	amazon_df = pd.DataFrame.from_dict(data)
	amazon_df['Title'].replace('', np.nan, inplace=True)
	amazon_df = amazon_df.dropna(subset=['Title'])
	amazon_df.to_csv("Amazon_data" + datetime.now().strftime("_%d_%m_%Y_%H_%M_%S") + ".csv", header=True, index=False)

	print(amazon_df)