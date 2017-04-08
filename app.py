
import os, json, re
import flask
import random

from flask import (
	Flask, 
	render_template, 
	redirect, 
	url_for, 
	request, 
	make_response,
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':  
		return render_template("Hangman.html")
	else:
		return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
	words = ['red', 'blue', 'green']
	random_word = (random.choice(words))
	return render_template("game.html",random_word=random_word)
	

if __name__ == "__main__":
	app.run(debug=True)