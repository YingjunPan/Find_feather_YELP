import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys

def save_review(filename,reviews):
	save_path = '/Users/Hussein/Desktop/demo/review/'+filename.split('_')[0]+'/'+filename.split('.')[0]+'/'
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	for i in range(len(reviews)):
		fw=open(save_path+filename.split('.')[0]+'_'+str(i)+'.txt','w')
		fw.write(reviews[i])
		fw.close()

def get_reviews(path):
	reviews = []
	file = open(path)
	f = file.read()
	soup = BeautifulSoup(f,'html.parser')
	body = soup.find('ul', class_ = "ylist ylist-bordered reviews")
	for li in body.find_all('li'):
		try:
			review = li.find('p', lang = 'en').text
			reviews.append(review)
		except AttributeError:
			continue
	file.close()
	return reviews

def parser():
	for (dirpath, dirnames, filenames) in os.walk('/Users/Hussein/Desktop/demo/HTML'):
		for filename in filenames:
			if filename.endswith('txt'):
				filepath = os.path.join(dirpath,filename)
				reviews = get_reviews(filepath)
				save_review(filename,reviews)
				print(filename,' done')

if __name__ == '__main__':
	parser()