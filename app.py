from flask import Flask, render_template
from flask_wtf import FlaskForm as Form 
from wtforms import StringField
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from wtforms.validators import InputRequired, URL
import joblib
from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import train_test_split
import os

import re



app = Flask(__name__)
app.config['SECRET_KEY']= os.urandom(24)

def trim(url):
    return re.match(r'(?:\w*://)?(?:.*\.)?([a-zA-Z-1-9]*\.[a-zA-Z]{1,}).*', url).groups()[0]

def getTokens(input):
    tokensBySlash = str(input.encode('utf-8')).split('/')
    allTokens = []
    for i in tokensBySlash:
        tokens = str(i).split('-')	
        tokensByDot = []
        for j in range(0,len(tokens)):
            tempTokens = str(tokens[j]).split('.')
            tokensByDot = tokensByDot + tempTokens
        allTokens = allTokens + tokens + tokensByDot
    allTokens = list(set(allTokens))
    if 'com' in allTokens:
        allTokens.remove('com')	
    return allTokens


class LoginForm(Form):
	url = StringField('Enter URL : ', validators=[InputRequired(), URL()])


@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		df = pd.read_csv(
        r"{}/data/spamurl.csv".format(os.getcwd()), encoding="latin-1")

		df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
    	# Features and Labels
		df['label'] = df['v1']
		df['message'] = df['v2']
		df.drop(['v1', 'v2'], axis=1, inplace=True)
		X = df['message']
		y = df['label']
        
		print(y)
		cv = CountVectorizer()
		X = cv.fit_transform(X)  # Fit the Data
		X_train, X_test, y_train, y_test = train_test_split(
			X, y, test_size=0.33, random_state=42)
		# Naive Bayes Classifier
		clf = MultinomialNB()
		clf.fit(X_train, y_train)
		clf.score(X_test, y_test)
		# prediction = model.predict(vectorizer.transform([trim(form.url.data)]))

		# if prediction[0] == 0:
		# 	#prediction = "NOT MALICIOUS"
		# 	return render_template("success.html", url = form.url.data, status = "Non Malicious")
		# else:
		# 	#prediction = "MALICIOUS"
		# 	return render_template("success.html", url= form.url.data, status = "Malicious")
		return render_template('success.html', url = form.url.data, prediction = "Malicious")
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
