#!/bin/bash
# debug.sh

name=${PWD##*/}

python3 -OO $name.py $*

# db="-db results.db"

# echo "Read"
# python3 -OO $name.py $db -re "{'test': {'description': 'Hello', 'world!': {'Welcome!': {}}}}" $*

# echo "Find"
# python3 -OO $name.py $db -fi test,world!,Welcome! $*

# echo "Search"
# python3 -OO $name.py $db -se -na ome -ds ome $*

# echo "Update"
# python3 -OO $name.py $db -ds update -up -ui 2 $*

# echo "Write"
# python3 -OO $name.py $db -wr -ui 1 $*

# echo "Delete"
# python3 -OO $name.py $db -de -ui 1 $*
