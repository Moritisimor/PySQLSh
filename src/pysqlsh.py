#!/usr/bin/env python
import os
import readline
import sqlite3
import sys

# Ansi Magic
redify = lambda x: f"\033[31m{x}\033[0m"
blueify = lambda x: f"\033[34m{x}\033[0m"
greenify = lambda x: f"\033[32m{x}\033[0m"
blackify = lambda x: f"\033[30m{x}\033[0m"
yellowify = lambda x: f"\033[33m{x}\033[0m"

if len(sys.argv) > 1:
    db = sqlite3.connect(sys.argv[1])
    PROMPT = f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(sys.argv[1])} {blackify(">>")} "
else:
    db_name = input(blueify("Enter DB Path: "))
    PROMPT = f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(db_name)} {blackify(">>")} "
    db = sqlite3.connect(db_name)

while True:
    try:
        cmd = input(PROMPT)
        crs = db.execute(cmd)
        db.commit()

        idx = 0
        for i in crs.fetchall():
            idx += 1
            print(f"{blueify("Record Nr.")} {yellowify(idx)} {greenify(i)}")

        if idx == 0:
            print(blackify("Void"))

    except sqlite3.OperationalError as e:
        print(redify(f"Error while executing command: {e}"))

    except KeyboardInterrupt:
        print("^C")

    except EOFError:
        print("Bye")
        sys.exit(0)
