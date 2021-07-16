# import libraries
import sys
import os
import urllib.request as req
import requests
import json
import sqlite3 as sql

# vaiables
path_to_file = sys.argv[1]
word_list = []
home = os.path.expanduser("~")
# directories paths
#dir_base = "/home/mhmd/Projects/python/Dictation Helper"
dir_base = f"{home}/.spell_helper"
dir_audio = f"{dir_base}/audio"
# database variables
## connect to the database or create one
conn = sql.connect(f'{dir_base}/database.db')
## create a curosr to communicte with the database
cur = conn.cursor()
# urls
url = "https://api.dictionaryapi.dev/api/v2/entries/en_US"

def init_database(conn, cur):
    # create words table
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS words(
                        id integer PRIMARY KEY,
                        word text NOT NULL,
                        audio_path text NULL
                )
                """ )
    # commit the changes
    conn.commit()

# check if the input arg is a file
if(os.path.isfile(path_to_file) is False):
   print("Please pass a file.")
   exit()
# check if the base directory exists
if(os.path.isdir(dir_base) is False):
    os.mkdir(dir_base)
# initalizing database
init_database(conn, cur)

# copy file line by line to an array
with open(path_to_file) as file:
   for line in file:
      # check the word doesn't contain blank space
      if len(line.split()) < 2:
         # remove \n from the end of each line
         word_list.append(line.rstrip())

# download json of each word in josn directory
print("Start downloading words:")
for i in range(len(word_list)):
    print(f"{i + 1}: Downloading the word \"{word_list[i]}\". ", end="")
    try:
        content = requests.get(f'{url}/{word_list[i]}').content
        dataset = json.loads(content)
        word = dataset[0]["word"]
        #check if the word has phonetics
        if not dataset[0]["phonetics"]:
            print(f'The word \"{word}\" doesn\'t have audio file.')

        elif(os.path.isfile(f'{dir_audio}/{word}.mp3') is False):
            url_audio = dataset[0]["phonetics"][0]["audio"]
            try:
                url_path = f"{dir_audio}/{word}.mp3"
                # donwlaod audio file
                req.urlretrieve(url_audio, url_path)
                cur.execute("INSERT INTO words VALUES (?,?,?)", (None, word, url_path))
                conn.commit()
                print("Word added to database.")
            except Exception as e:
                print("Failed to download audio file.")
        else:
           print(f"The word \"{word}\" already exists.")
    except Exception as e:
        print(", Failed to fetch JSON.")

conn.close()
