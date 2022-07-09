# jisho-cli
JP to EN dictionary that is simple, fast and local.
![alt text](https://github.com/amyeo/jisho-cli/blob/master/screenshot.png?raw=true)

Uses JMdict as a data source.

# What makes it different?
**All** the source code, including the print statements and console formatting only adds up to ~250 lines of code. There are only 2 files: bootstrap.py and command.py

`bootstrap.py` downloads JMdict, converts the data and builds the index, while `command.py` is the interactive cli lookup tool

## Fast startup and lookup
When `command.py` is executed, the `LOOKUP> ` prompt loads **instantly**. Due to a **very simple indexing and lookup algorithm**, word lookups also take less than 0.01 seconds of system time to complete (practical/average case).

# Dependencies
```
rich
```

# Pager
Uses the system's pager to display all results for easier reading. Assumes a reasonably modern Linux system that uses `less`. Source code can be easily edited for other scenarios.

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
