import json
import bson
import pickle
import os
import urllib.request
import gzip
import shutil

print("This package uses the JMdict/EDICT and KANJIDIC dictionary files. These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence. \n")

print("checking for existence of JMdict gz file ...")
if not os.path.exists("JMdict.gz"):
    url = 'ftp://ftp.edrdg.org/pub/Nihongo//JMdict.gz'
    print("> does not exist. need to download ...")
    print(f"> issues? download manually at {url}")
    urllib.request.urlretrieve(url, 'JMdict.gz')

assert os.path.exists("JMdict.gz")

print("extracting files from archive ...")
with gzip.open('JMdict.gz', 'rb') as f_in:
    with open('JMdict', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

assert os.path.exists("JMdict")

print("parsing JMdict XML ...")

import xml.etree.ElementTree as ET
tree = ET.parse('JMdict')
root = tree.getroot()

import dbm
db = dbm.open('word_database.db','n')

ENTRIES = [] # actual dictionary entries
LOOKUP = {} # for building the search index

print("converting data ...")

for child in root:
    ENTRY = {}
    MAPPING = {
        "ent_seq": "id",
        "keb": "kanji_list",
        "reb": "kana_list",
        "gloss": "translation_dict_list",
    }


    for entry in child.iter():
        assert type(entry.attrib) == dict
        if entry.tag in MAPPING:
            if entry.tag == "gloss":
                lang = entry.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                if MAPPING[entry.tag] not in ENTRY:
                    ENTRY[MAPPING[entry.tag]] = {}
                if lang not in ENTRY[MAPPING[entry.tag]]:
                    ENTRY[MAPPING[entry.tag]][lang] = []
                ENTRY[MAPPING[entry.tag]][lang].append(entry.text)
            elif entry.tag == "keb" or entry.tag == "reb":
                if MAPPING[entry.tag] not in ENTRY:
                    ENTRY[MAPPING[entry.tag]] = []
                ENTRY[MAPPING[entry.tag]].append(entry.text)
            elif entry.tag == "ent_seq":
                ENTRY[MAPPING[entry.tag]] = int(entry.text)

    
    db[str(ENTRY["id"])] = bson.BSON.encode(ENTRY)
    ENTRIES.append(ENTRY)

db.close()

#phase 2: build index
#ENTRIES var can be used
for entry in ENTRIES:
    for chr_list in ["kanji_list","kana_list"]:
        if chr_list in entry:
            kanji_strs = entry[chr_list]
            for kanji in kanji_strs:
                for c in str(kanji):
                    char_code = int(ord(c))
                    if char_code not in LOOKUP:
                        LOOKUP[char_code] = set()
                    LOOKUP[char_code].add(entry['id'])

print("writing index db ...")
dbfile = open('word_index.pickle', 'wb')
pickle.dump(LOOKUP, dbfile)
dbfile.close()

print("parsing XML done. deleting the extracted file to leave only the compressed version on disk ...")
os.remove('JMdict')

print("done.")
