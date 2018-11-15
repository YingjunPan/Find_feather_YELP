import pandas as pd
from sklearn.cross_validation import train_test_split
import re

def model(x_train,y_train):
	pool = []
	for i in y_train:
		item = i.strip().split(',')
		pool.extend(item)
	pool = set(pool)
	return pool

def predict(pool,x_test,y_test):
	result = {}
	for each in x_test:
		feature = []
		for word in re.sub("[^\w]", " ",  each).split():
			if word in pool:
				feature.append(word)
		feature = list(set(feature))
		result[each] = feature
	df_result = pd.DataFrame.from_dict(data = result,orient='index')
	return df_result


def output():
	df = pd.read_csv('/Users/Hussein/Desktop/demo/data.csv',encoding = "ISO-8859-1")
	df = df[df['attributes'] != 'na'].dropna()
	x = df['review'].as_matrix()
	y = df['attributes'].as_matrix()
	x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.1)
	pool = model(x_train,y_train)
	df_result = predict(pool,x_test,y_test)
	df_result.to_csv('result.csv')


# count_vect = CountVectorizer()
# X_counts = count_vect.fit_transform(x)
# Y_counts = count_vect.fit_transform(y)

# x_train, x_test, y_train, y_test = train_test_split(X_counts,Y_counts,test_size = 0.1)

# print(y_train.shape)

# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# clf = MultinomialNB().fit(X_train_counts,Y_train_counts)

# text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])

# text_clf = text_clf.fit(x,y)


if __name__ == '__output__':
	output()