from __future__ import print_function
from flask_sqlalchemy import SQLAlchemy
from random import randint
import os, json, re
import flask
import random
import sys
import tmdbsimple as tmdb
import requests

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hellokitty@localhost/flask_hangman'
db=SQLAlchemy(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
tmdb.API_KEY = '3ed0121bfe2f634e5aff3cc6c826fa8a'

class GameInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True) 
	difficulty = db.Column(db.String(80))
	numtries = db.Column(db.Integer)
	status = db.Column(db.String(10))

	def __init__(self,difficulty,numtries,status):
		self.difficulty = difficulty
		self.numtries = numtries
		self.status = status

def get_word(difficulty_level):
	while True:
		random_num = randint(5,750) #4
		temp_random_word = tmdb.Movies(random_num)
		try:
			response = temp_random_word.info()
		except requests.exceptions.HTTPError as err:
			continue
		temp_random_word = temp_random_word.title
		print(temp_random_word, file=sys.stderr)
		if re.match('^[^<!@#$%^&*():;0-9>]+$', temp_random_word):
			session['correct_answer']=temp_random_word
			if difficulty_level=='Normal' and len(set(temp_random_word))<=7:
				session['random_word']=temp_random_word.lower()
				break
			elif difficulty_level=='Hard' and len(set(temp_random_word))>7 and len(set(temp_random_word))<=10:
				session['random_word'] = temp_random_word.lower()
				break

def convert_letter(word):
    new_word = word
    for i in range(0, len(word)):
        if ord(word[i]) != 32:
            new_word = new_word.replace(word[i], '_ ')
    print(new_word, file=sys.stderr)
    return new_word

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':  
		return render_template("Hangman.html")
	else:
		if request.form['difficulty'] == 'Normal':
			session['difficulty_level']=request.form['difficulty']
			return redirect(url_for('main'))
		if request.form['difficulty'] == 'Hard':
			session['difficulty_level']=request.form['difficulty']
			return redirect(url_for('main'))
		if request.form['form1']== 'Submit':
			return redirect(url_for('setup'))

@app.route('/setup', methods=['GET','POST'])
def setup():
	get_word(session['difficulty_level'])
	session['Word_length'] = len(session['random_word'])
	session['Word_list'] = list(session['random_word']) 
	session['Word_list'] = [item.lower() for item in session['Word_list']]
	session['blank_word'] = convert_letter(session['random_word'])
	print(session['blank_word'], file=sys.stderr)
	session['blank_list'] = [' ']*session['Word_length']
	session['visual_blank_word'] = ''
	for i in session['random_word']:
  		x = re.sub(r"\S", '_ ', i)
  		session['visual_blank_word'] += x
	session['visual_blank_list'] = session['visual_blank_word'].split(" ")
	session['Counter'] = 0
	session['used_letters']=[]
	session['incorrect_letters']=[]
	session['incorrect_letters_counter']=0
	return render_template("setup.html",random_word=session['random_word'],blank_list=session['blank_list'],
		Word_list=session['Word_list'],blank_word=session['blank_word'],Word_length=session['Word_length'])

@app.route('/game', methods=['GET','POST'])
def game():
	if request.method == 'POST': 
		if session['Counter'] < 12: #change 12 stand 9
			session['textbox']=request.form['text']
			visual_blank_word=session.get('visual_blank_word',None)
			Word_list=session.get('Word_list',None)
			blank_list=session.get('blank_list',None)
			visual_blank_list=session.get('visual_blank_list',None)
			print(blank_list, file=sys.stderr)
			letter_choice=session.get('textbox',None)
			letter_choice=letter_choice.lower()
			used_letters=session.get('used_letters',None)
			incorrect_letters=session.get('incorrect_letters',None)
			incorrect_letters_counter=session.get('incorrect_letters_counter',None)
			#cross letter from list
			print(visual_blank_word, file=sys.stderr)
			if re.match("^[a-z]*$", letter_choice) and len(letter_choice) == 1:
				if letter_choice not in session['random_word']:
					print(visual_blank_word, file=sys.stderr)
					incorrect_letters.extend(letter_choice)
					session['incorrect_letters_counter']=session['incorrect_letters_counter']+1
					print(visual_blank_word, file=sys.stderr)
				if letter_choice not in used_letters:
					used_letters.extend(letter_choice)
					for i, j in enumerate(Word_list):
						if j==letter_choice:
							blank_list[i]=letter_choice
							visual_blank_list[i]=letter_choice
							visual_blank_word = ' '.join(visual_blank_list)
							session['visual_blank_word'] = visual_blank_word
							print(blank_list, file=sys.stderr)
							print(Word_list, file=sys.stderr)
							print(letter_choice, file=sys.stderr)
							print(session['random_word'], file=sys.stderr)
							if blank_list == Word_list:
								print(blank_list, file=sys.stderr)
								print(Word_list, file=sys.stderr)
								session['game_status'] = 'won'
								return redirect(url_for('done'))
					session['Counter'] = session['Counter'] + 1
					print(visual_blank_word, file=sys.stderr)
					return render_template("game.html",visual_blank_word=visual_blank_word,blank_list=session['blank_list'], letter_choice=letter_choice, used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
				else:
					error="You have already tried the letter '" + letter_choice + "', try agian"
					return render_template("game.html",visual_blank_word=visual_blank_word, blank_list=session['blank_list'],error=error,used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
			else:
				error="Error! Only letters a-z and 1 characters allowed!, try again"
				return render_template("game.html",visual_blank_word=visual_blank_word, blank_list=session['blank_list'],error=error,used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
		else:
			session['game_status'] = 'lost'
			return redirect(url_for('done'))

@app.route('/done', methods=['GET','POST'])
def done():
	if session['game_status'] == 'lost':
		message=" You " +session['game_status'] +" and a total of " + str(session['Counter']) + " tries. The correct answer was " +session['correct_answer']+ " . Would you like to try again?"
	else:
		message=" You " +session['game_status'] +" and a total of " + str(session['Counter']) + " tries. Would you like to try again?"
	gameinfo = GameInfo(session['difficulty_level'],session['Counter'],session['game_status'])
	db.session.add(gameinfo)
	db.session.commit()
	if request.method == 'POST':  
		if request.form['form1'] == 'Try Again':
			return redirect(url_for('setup'))
		if request.form['quit'] == 'Quit Game':
			return redirect(url_for('main'))
	return render_template("done.html",message=message)

@app.route('/about', methods=['GET','POST'])
def about():
	return render_template("about.html")

if __name__ == "__main__":
	app.run(debug=True)

"""
fix hangman image->bootstrap
block letters from a-z
show poster
reduce to 2 buttons
move input down

add option to guess full name

counting w/l
not chossing word after
no pt if use hint
database
hint

button on done broken
counter add when guess smae letter twice

Finished
api not work
change button color
add link for help and contact/about
"""