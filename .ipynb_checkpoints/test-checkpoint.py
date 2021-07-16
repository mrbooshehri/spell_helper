# test section

import json
import urllib.request as req
from playsound import playsound
import time

# open the json file
word_json = open ('word.json',)
# get url of the word
data = json.load(word_json)
word = data[0]["word"]
url = data[0]["phonetics"][0]["audio"]
# close the json file
word_json.close
# print the url to check
#print(url)
# donwlaod audio file
req.urlretrieve(url,f'./{word}.mp3')

# print welcome messge
print("Listen to the sound and write it.")
# short delay before paly the audio file
time.sleep(1)
print(word)
# play the audio file
playsound(f'./{word}.mp3')
# read from input
user = input("Word: ")
# cheak the correcness
if (user == word):
    print ("Great!")
else:
    print ("That's wrong, try again")
