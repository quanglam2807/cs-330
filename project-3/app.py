from flask import Flask
from flask import request
from flask import Response
from flask import render_template

import string
import json

app = Flask(__name__)

alphabet = list(string.ascii_lowercase)

# https://www.thewordfinder.com/scrabble-point-values.php
scores = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10
}

def getWordScore(word): 
    score = 0
    for i in range(len(word)):
        score = score + scores[word[i]]

    return score

def isValid(word, letters):
    lst = list(letters)
    
    for i in range(len(word)):
        if word[i] in lst:
            lst.remove(word[i])
        elif '*' in lst and word[i] in alphabet:
            lst.remove('*')
        else:
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        letters = []

        # Only one asterisk
        if len(request.form['letter1']) > 0: letters.append(request.form['letter1'])
        if len(request.form['letter2']) > 0: 
            if not ('*' in letters and request.form['letter2'] == '*'):
                letters.append(request.form['letter2'])    
        if len(request.form['letter3']) > 0: 
            if not ('*' in letters and request.form['letter3'] == '*'):
                letters.append(request.form['letter3'])
        if len(request.form['letter4']) > 0: 
            if not ('*' in letters and request.form['letter4'] == '*'):
                letters.append(request.form['letter4'])
        if len(request.form['letter5']) > 0:
            if not ('*' in letters and request.form['letter5'] == '*'):
                letters.append(request.form['letter5'])
        if len(request.form['letter6']) > 0: 
            if not ('*' in letters and request.form['letter6'] == '*'):
                letters.append(request.form['letter6'])
        if len(request.form['letter7']) > 0: 
            if not ('*' in letters and request.form['letter7'] == '*'):
                letters.append(request.form['letter7'])

        enableExistingLetters= request.form.get('enableExistingLetters')
        existingLetters = '' if request.form.get('existingLetters') is None else request.form.get('existingLetters')
        dictCode = request.form['dictCode']

        # dictPath = 'american-english' if dictCode == 'en-gb' else 'british-english' 
        dictPath = '/usr/share/dict/american-english' if dictCode == 'en-gb' else '/usr/share/dict/british-english' 
        f = open(dictPath, 'r')
        dictLst = [x.lower() for x in f.read().split('\n')]

        words = set([])

        for word in dictLst:
            if len(word) < 2:
                continue

            if isValid(word, letters):
                words.add(word)

            if enableExistingLetters == 'on':
                # Case 1
                for l in list(existingLetters):
                    if l in word and isValid(word.replace(l, ''), letters):
                        words.add(word)

                # Case Prefix
                if word.endswith(existingLetters):
                    if isValid(word[:-len(existingLetters)], letters):
                        words.add(word)
                
                # Case Suffix
                if word.startswith(existingLetters):
                    if isValid(word[len(existingLetters):], letters):
                        words.add(word)

        results = []
        for word in words:
            results.append({
                'word': word,
                'length': len(word),
                'score': getWordScore(word)
            })

        return render_template(
            'index.html', 
            results=results, 
            letter1=request.form['letter1'],
            letter2=request.form['letter2'],
            letter3=request.form['letter3'],
            letter4=request.form['letter4'],
            letter5=request.form['letter5'],
            letter6=request.form['letter6'],
            letter7=request.form['letter7'],
            dictCode=dictCode,
            enableExistingLetters=enableExistingLetters,
            existingLetters=existingLetters
        )
    return render_template('index.html')


if __name__ == '__main__':
    app.run()