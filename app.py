from __future__ import print_function
import os, json, re
import flask
import random
import sys

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

def get_word(words,difficulty_level):
	while True:
		temp_random_word =(random.choice(words)).lower()
		if difficulty_level=='Normal' and len(set(temp_random_word))<=6:
			session['random_word']=temp_random_word
			break
		elif difficulty_level=='Hard' and len(set(temp_random_word))>6:
			session['random_word'] = temp_random_word
			break


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
	text_file = open('Hardwords.txt',"r")
	words = text_file.read().split(',')
	get_word(words,session['difficulty_level'])
	text_file.close()
	session['Word_length'] = len(session['random_word'])
	session['blank_word'] = "_ " * session['Word_length']
	session['blank_list'] = session['blank_word'].split()
	session['Word_list'] = list(session['random_word'])  
	session['Counter'] = 0
	session['used_letters']=[]
	session['incorrect_letters']=[]
	session['incorrect_letters_counter']=0
	return render_template("setup.html",random_word=session['random_word'],
		Word_list=session['Word_list'],blank_word=session['blank_word'],words=words,Word_length=session['Word_length'])

@app.route('/game', methods=['GET','POST'])
def game():
	if request.method == 'POST': 
		if session['Counter'] < 9: #change 12 stand
			session['textbox']=request.form['text']
			#print(session['textbox'])
			Word_list=session.get('Word_list',None)
			blank_list=session.get('blank_list',None)
			letter_choice=session.get('textbox',None)
			letter_choice=letter_choice.lower()
			used_letters=session.get('used_letters',None)
			incorrect_letters=session.get('incorrect_letters',None)
			incorrect_letters_counter=session.get('incorrect_letters_counter',None)
			#cross letter from list
			if re.match("^[a-z]*$", letter_choice) and len(letter_choice) == 1:
				if letter_choice not in session['random_word']:
					print('Hello world!DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', file=sys.stderr)
					incorrect_letters.extend(letter_choice)
					session['incorrect_letters_counter']=session['incorrect_letters_counter']+1
				if letter_choice not in used_letters:
					print('Hello world!BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB', file=sys.stderr)
					used_letters.extend(letter_choice)
					for i, j in enumerate(Word_list):
						if j==letter_choice:
							blank_list[i]=letter_choice
							print(letter_choice, file=sys.stderr)
							print(session['random_word'], file=sys.stderr)
							if blank_list == Word_list:
								session['game_status'] = 'won'
								return redirect(url_for('done'))
					session['Counter'] = session['Counter'] + 1
					return render_template("game.html",blank_list=session['blank_list'], letter_choice=letter_choice, used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
				else:
					print('Hello world!AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', file=sys.stderr)
					error="You have already tried the letter '" + letter_choice + "', try agian"
					return render_template("game.html",blank_list=session['blank_list'],error=error,used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
			else:
				error="Error! Only letters a-z and 1 characters allowed!, try again"
				#session['Counter'] = session['Counter'] + 1
				return render_template("game.html",blank_list=session['blank_list'],error=error,used_letters=used_letters,incorrect_letters=incorrect_letters,incorrect_letters_counter=session['incorrect_letters_counter'])
		else:
			session['game_status'] = 'lost'
			return redirect(url_for('done'))

@app.route('/done', methods=['GET','POST'])
def done():
	message=" You " +session['game_status'] +". You had a total of " + str(session['Counter']) + " tries. Would you like to try again?"
	if request.method == 'POST':  
		print('Hello world!HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH', file=sys.stderr)
		if request.form['form1'] == 'Try Again':
			print('Hello world!IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', file=sys.stderr)
			return redirect(url_for('setup'))
		if request.form['quit'] == 'Quit Game':
			print('Hello world!UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU', file=sys.stderr)
			return redirect(url_for('main'))
	return render_template("done.html",message=message)

if __name__ == "__main__":
	app.run(debug=True)

"""
block letters from a-z
visual hangman image
make the site look good
api/topic/hint
topic
counting w/l
not chossing word after
no pt if use hint
database
"""

