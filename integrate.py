
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from flask import Flask, render_template, url_for, request
import pickle


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	data=pd.read_csv('train.tsv', sep='\t')
        
		
	token = RegexpTokenizer(r'[a-zA-Z0-9]+')
	cv = CountVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)
	text_counts= cv.fit_transform(data['Phrase'])
		
	X_train, X_test, y_train, y_test = train_test_split(
		text_counts, data['Sentiment'], test_size=0.3, random_state=1)
		
		
	clf = MultinomialNB().fit(X_train, y_train)
	predicted= clf.predict(X_test)
	print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))
	
	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = cv.transform(data).toarray()
		my_prediction = clf.predict(vect)
	return render_template('result.html',prediction = my_prediction)

if __name__ == '__main__':
	app.run(debug=True)