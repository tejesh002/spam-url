from flask import Flask, render_template
from flask_wtf import FlaskForm as Form 
from wtforms import StringField
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from wtforms.validators import InputRequired, URL
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
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


def extractUrl(data):
    url = str(data)
    extractSlash = url.split('/')
    result = []
    
    for i in extractSlash:
        extractDash = str(i).split('-')
        dotExtract = []
        
        for j in range(0,len(extractDash)):
            extractDot = str(extractDash[j]).split('.')
            dotExtract += extractDot
            
        result += extractDash + dotExtract
    result = list(set(result))

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		url = pd.read_csv(
        r"{}/data/spamurl.csv".format(os.getcwd()), encoding="latin-1")

		url['is_spam'] = url['is_spam'].apply(lambda x : 1 if x == "True" in x else 0)

	
		cv = CountVectorizer(tokenizer=extractUrl)
    
		vect = cv.transform([trim(form.url.data)])
                
                
		print(vect) 


	
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
