import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

def get_html(url):
	for i in range(5):
		try:
			r = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'},timeout = 30)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
			break
		except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
			print ('failed attempt',i)
			time.sleep(2)

def get_link(html):
	# links = []
	# name = []
	soup = BeautifulSoup(html,'html.parser')
	chunk = soup.find_all('a',{'class':'biz-name js-analytics-click','data-analytics-label':"biz-name"})
	for a in chunk:
		if 'osq=Restaurants' in a['href']:
			restaurants[a.contents[0].string] = "https://www.yelp.com" + a['href']
			# links.append(a['href'])
			# name.append(a.contents[0].string)
	# df = pd.DataFrame(list(restaurants.items()), columns = ['Restaurant','Link'])
	# df.to_csv('Restaurants.csv',index = False)
	# return restaurants
def generate_csv():
	print('Generating restaurants list\n')
	global restaurants
	restaurants = {}
	ori_url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Seattle,+WA&"
	cuisine = ['mexican','chineses','italian']
	for i in range(len(cuisine)):
		for k in range(10):
			url = ori_url + 'start=0&cflt=' + cuisine[i]
			if k:
				url = ori_url + 'start=' + str(k) + '0&cflt=' + cuisine[i]
			html = get_html(url)
			get_link(html)
	df = pd.DataFrame(list(restaurants.items()), columns = ['Restaurant','Link'])
	df.to_csv('restaurants.csv',index = False)

def get_reviews():
	generate_csv()
	df = pd.read_csv('restaurants.csv')
	ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
	for index, row in df.iterrows():
		# save_path = '/Users/Hussein/Desktop/660-Web Analytics/Final project/'
		for i in range(10):
			save_path = ROOT_DIR + '/HTML/' + row['Restaurant']
			if not os.path.exists(save_path):
				os.makedirs(save_path)
			rev_url = row['Link']
			if i:
				rev_url = row['Link'].split('?')[0]+'?start=' + str(i*20)
			rev_html = get_html(rev_url)
			soup = BeautifulSoup(rev_html,'html.parser')
			if (soup.find('ul', class_ = "ylist ylist-bordered reviews")).find('p', lang = 'en'):
				save_html = soup.prettify("utf-8")
				with open(save_path+'/'+row['Restaurant'] + '_' +str(i)+'.txt',"wb") as file:
					file.write(save_html)
				print(row['Restaurant']+' '+str(i)+' done')
	# for link in links:
	# 	for i in range(10):
	# 		restaurant_url = "https://www.yelp.com" + link
	# 		if i:
	# 			restaurant_url = "https://www.yelp.com" + link + "?start=" + str(i*20)
	# 		restaurant_html = get_html(restaurant_url)
	# 		soup = BeautifulSoup(restaurant_html,'html.parser')
	# 		save_html = soup.prettify("utf-8")
	# 		save_path = ''
	# 		with open("output.txt", "wb") as file:
	# 			file.write(new_html)
			# for li in soup.find_all('ul', class_ = "ylist ylist-bordered reviews"):
			# 	li.find('p', lang = 'en')







if __name__ == '__main__':
	get_reviews()