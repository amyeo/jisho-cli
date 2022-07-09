# jisho-cli
JP to EN dictionary that is simple, fast and local.

![alt text](https://github.com/amyeo/jisho-cli/blob/master/screenshot.png?raw=true)

Uses JMdict as a data source.

# What makes it different?
**All** the source code, including the print statements and console formatting only adds up to ~250 lines of code. There are only 2 files: bootstrap.py and command.py

`bootstrap.py` downloads JMdict, converts the data and builds the index, while `command.py` is the interactive cli lookup tool

## Fast startup and lookup
When `command.py` is executed, the `LOOKUP> ` prompt loads **instantly**. Due to a **very simple indexing and lookup algorithm**. Word lookups also take less than 0.01 seconds of system time to complete (practical/average case).

The tradeoff here is memory usage. During lookup, it can be from 77 MiB - 157 MiB depending on the query. This is still an improvement from outright loading the entire database into memory, which consumes ~5 GiB of RAM based on my testing. (which is why this program was created). It is possible to decrease memory usage even further, however priority is startup and lookup speed, which makes memory usage a fairly reasonable compromise.

## Custom search/lookup algorithm
A straightforward list-based word index for searching would consist of all the kanji and kana readings of each word. Considering around 100,000+ entries with multiple kanji and kana readings, the "index" represented as a list means for every lookup, the program would need to loop the whole length of the list.

My proposed solution for this is dead simple: shrink the list size from 100,000+ to something very managable. For this, the index is represented by a dictionary with each key representing each character of each word. In the case of Japanese, each letter or character is only shared by a few words. For example, 駅(eki) is only present on 80 entries in the dictionary. Thus, from 100,000+ the search has been reduced to 80.

# Dependencies
```
rich
```

# Pager
Uses the system's pager to display all results for easier reading. Assumes a reasonably modern Linux system that uses `less`. Source code can be easily edited for other scenarios.

# Wildcard/? Queries
Wildcard queries using "?" are supported. For example ?会 will return words such as 教会 and 協会.

# Usage example
```
$ python command.py
Local Jisho Interactive Lookup
Consult README for documentation.
This package uses the JMdict/EDICT and KANJIDIC dictionary files. These files are the
property of the Electronic Dictionary Research and Development Group, and are used in
conformance with the Group's licence.
EOF or ctrl+c to quit

LOOKUP > : 電車

 [#0] 1443530 ────────────────────────────────────────────────────────────────────────────

   電車
   でんしゃ
  ╭────────────────────────────────────────────────────────────────────────────────────╮
  │ train     electric train                                                           │
  ╰────────────────────────────────────────────────────────────────────────────── eng ─╯

39 results in 0.000191533000000 seconds.
Showing only first. Display all results? [y/n]: n
LOOKUP > :
```

# JMdict attribution
This publication has included material from the JMdict (EDICT, etc.) dictionary files in accordance with the licence provisions of the Electronic Dictionaries Research Group. See http://www.edrdg.org/ 
