# import libraries
import os
import sqlite3 as sql
from playsound import playsound
import time

# vaiables
word_list = []
right_words = []
wrong_words = []
home = os.path.expanduser("~")
# directories paths
#dir_base = "/home/mhmd/Projects/python/Dictation Helper"
dir_base = f"{home}/.spell_helper"
dir_audio = f"{dir_base}/audio"

db = "database.db"

print(dir_base)
# check if the database exist
if (os.path.isfile(f'{dir_base}/{db}') is False):
    print("Database doesn't exist, plese run the \"downloder.py\" first.")
    exit()

# database variables
## connect to the database or create one
conn = sql.connect(f'{dir_base}/{db}')
## create a curosr to communicte with the database
cur = conn.cursor()

cur.execute("SELECT word, audio_path FROM words ORDER BY random() LIMIT 5")
conn.commit()

# fetch data to array list
word_list = cur.fetchall()

for row in word_list:
    # play the audio file
    playsound(row[1])
    # read from input
    user = input("Enter the word you heared: ")
    # cheak the correcness
    if user == row[0]:
        right_words.append(user)
    else:
        wrong_words.append(f'r:{row[0]} , w:{user}')

print(len(right_words), "right answers: ", right_words)
print(len(wrong_words), "wrong answers: ", wrong_words)
print(f'Correctnes ratio: {(len(right_words)/len(word_list))*100}')
conn.close()
