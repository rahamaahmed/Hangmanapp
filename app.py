
import os, json, re
import flask
import random

from flask import (
	Flask, 
	render_template, 
	redirect, 
	url_for, 
	request, 
	session,
	make_response,
)

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':  
		return render_template("Hangman.html")
	else:
		return redirect(url_for('setup'))

@app.route('/setup', methods=['GET','POST'])
def setup():
	words = ['red', 'blue', 'green']
	session['random_word'] = (random.choice(words))
	session['Word_length'] = len(session['random_word'])
	session['blank_word'] = "_ " * session['Word_length']
	session['blank_list'] = session['blank_word'].split()
	session['Word_list']= list(session['random_word'])  
	return render_template("setup.html",random_word=session['random_word'],
		Word_list=session['Word_list'],blank_list=session['blank_list'])
	

@app.route('/game', methods=['GET','POST'])
def game():
	if request.method == 'POST': 
		session['textbox']=request.form['text']
		#print(session['textbox'])
		Word_list=session.get('Word_list',None)
		blank_list=session.get('blank_list',None)
		letter_choice=session.get('textbox',None)
		for i, j in enumerate(Word_list):
			if j==letter_choice:
				blank_list[i]=letter_choice
		return render_template("game.html",blank_list=session['blank_list'])
	#textbox = session.get('textbox', None)
	#return render_template("game.html",textbox=textbox)

if __name__ == "__main__":
	app.run(debug=True)

"""
one char lowercase tell if wrong
limited chances and visual image
get words from word api
choose diffculty
topic
try again
you won/lost
deploy app to heroku"""