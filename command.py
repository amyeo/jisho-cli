"""
the pretty cli friendly interactive version
"""

from difflib import SequenceMatcher
import bson
import pickle
import dbm
import readline
import time
import os

os.environ["MANPAGER"] = "less -r"

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from rich.prompt import Confirm, Prompt
console = Console()

#check if files exist
if not os.path.exists("word_database.db") or not os.path.exists("word_index.pickle"):
    console.print("FATAL: One or more of the required db and index files are missing. If this is your first time, please run bootstrap.py to download and build the dictionary data. \nYou may want to run it again in case of missing files or corruption.")
    exit()

db = dbm.open('word_database.db','r')

index_dbfile = open('word_index.pickle', 'rb')
LOOKUP = pickle.load(index_dbfile)

def find_candidates(user_input):
    results = None
    for c in user_input:
        char_code = int(ord(c))
        if char_code in LOOKUP and char_code != '?':
            if results is None:
                results = set(LOOKUP[char_code])
            else:
                results = results.intersection(set(LOOKUP[char_code]))
    return results

def display_results(results):
    for i, r in enumerate(results):
        console.rule(f" \[#{i}] {r['id']}", style="yellow", align="left")
        console.print()
        table = Table.grid(pad_edge=True, padding=(0,2,0,3))
        for chr_list in ["kanji_list", "kana_list"]:
            if chr_list in r:
                table.add_row(*r[chr_list], style="bold bright_green")
        console.print(table)
        for lang, entries in r["translation_dict_list"].items():
            if lang == "eng":
                console.print(Padding(Panel(Columns(entries, equal=False, align="left", padding=(0,2,0,5)), subtitle=lang, 
                subtitle_align="right"),(0,2,0,2)))
        console.print()

def get_question_sub(user_input_string, result_entry):
    import re
    lens = []
    new_user_input = str(user_input_string).replace('?','.*')
    for chr_list in ["kanji_list","kana_list"]:
        if chr_list in result_entry:
            for k in result_entry[chr_list]:
                matches = re.findall(new_user_input, k)
                for m in matches:
                    if len(m) == len(user_input_string):
                        lens.append(len(k))   
    return max(lens) if len(lens) > 0 else None


console.print("Local Jisho Interactive Lookup")
console.print("Consult README for documentation.", style="dim")
console.print("This package uses the JMdict/EDICT and KANJIDIC dictionary files. These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence. ", style="dim")
console.print("EOF or ctrl+c to quit",style="dim")
console.print()

while True:
    user_input = None
    try:
        user_input = Prompt.ask("[bold dodger_blue1]LOOKUP > ")
    except (EOFError, KeyboardInterrupt) as e:
        print("Bye")
        db.close()
        exit()
    console.print()

    assert user_input is not None

    st = time.process_time()
    results = find_candidates(user_input)
    et = time.process_time()
    res = et - st

    if results is None:
        console.print("[bold red]ERROR[/]: No parsable characters in input. (Example valid input: 電気 or 気?車)")
        continue

    results = [bson.BSON.decode(db[str(r)]) for r in results]

    """
    deal with 2 types of searches here
    type 1 = normal = sort by similarity
    type 2 = ? = question marks in words indicate placeholders
     - must respect overall substring length
     - sort for the results is based on length. the shorter ones go first
    """
    if "?" in user_input:
        new_results = []
        for r in results:
            shortest_len = get_question_sub(user_input, r)
            if shortest_len is not None:
                r["shortest_len"] = shortest_len
                new_results.append(r)
        results = sorted(new_results, key=lambda k: k['shortest_len'], reverse=False)
    else:
        #calculate string similarity
        for r in results:
            s_score = -1
            for chr_list in ["kanji_list","kana_list"]:
                if chr_list in r:
                    for k in r[chr_list]:
                        c_score = SequenceMatcher(None, user_input, k).ratio()
                        if c_score > s_score:
                            s_score = c_score
                    r["similarity"] = s_score
        results = sorted(results, key=lambda k: k['similarity'], reverse=True)

    display_results(results[:1])
    console.print(f"{len(results)} results in {res:.15f} seconds.",style="dim")
    if len(results) > 1:
        display_more = Confirm.ask("Showing only [bold red]first[/]. Display all results?")
        if display_more:
            with console.pager(styles=True):
                display_results(results)
db.close()
