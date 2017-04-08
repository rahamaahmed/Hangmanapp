
import os, json, re
import flask

from flask import (
	Flask, 
	session, 
	render_template, 
	redirect, 
	url_for, 
	request, 
	make_response,
)

app = Flask(__name__)

@app.route('/')
def index():
	session.clear()
	return render_template("Hangman.html")

@app.route('/game', methods=['GET', 'POST'])
def game():
	 words = ['red', 'blue', 'green']
	 random_word = (random.choice(words))
	 return render_template("Game.html",random_word)