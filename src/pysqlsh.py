#!/usr/bin/env python
import readline
import sqlite3
import sys

# Ansi Magic
redify = lambda x: f"\033[31m{x}\033[0m"
blueify = lambda x: f"\033[34m{x}\033[0m"
greenify = lambda x: f"\033[32m{x}\033[0m"
blackify = lambda x: f"\033[30m{x}\033[0m"
yellowify = lambda x: f"\033[33m{x}\033[0m"
boldify = lambda x: f"\033[1m{x}\033[0m"


def multiline_input(prompt: str) -> str:
    buf = ""
    while True:
        if buf == "":
            line = input(prompt)
        else:
            line = input(blueify("\t\t... "))

        buf += line.rstrip(";").strip() + " "
        if line.endswith(";"):
            return buf.strip()


def exec_statement(stmt: str, db: sqlite3.Connection):
    try:
        crs = db.execute(stmt)
        db.commit()

        idx = 0
        for i in crs.fetchall():
            idx += 1
            print(f"{blueify("Record Nr.")} {yellowify(idx)} {greenify(i)}")

        if idx == 0:
            print(blackify("Void"))
    except sqlite3.OperationalError as e:
        print(redify(f"Error while executing command: {e}"))


# exec_builtin works by trying to match cmd with a builtin, and, if found, returns True
# The return value can be used by the caller to determine whether or not it should execute
# cmd as a regular SQL statement.
def exec_builtin(cmd: str, db: sqlite3.Connection) -> bool:
    match cmd.split():
        case []:
            return True
        
        case [".clear"]:
            print("\033[H\033[2J\033[3J")
            return True
        
        case [".exit"]:
            print(blueify("Bye"))
            sys.exit(0)
            return True
        
        case [".tables"]:
            crs = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
            print(yellowify("Tables:"))
            for i in crs.fetchall():
                print(f"{blueify("->")} {greenify(i[0])}")

            return True
        
        case [".schema"]:
            crs = db.execute("SELECT name, sql FROM sqlite_master")
            print(yellowify("Schema:"))
            for i in crs.fetchall():
                print(f"{blueify("->")} {greenify(i[0])}{blackify(":")} {yellowify(i[1])}")

            return True
        
        case [".schema", tbl]:
            try:
                # Could lead to SQL injection but idc anymore
                crs = db.execute(f"SELECT sql FROM sqlite_master WHERE name = '{tbl}'")
                result = crs.fetchone()
                if result is None:
                    print(redify(f"No such table '{tbl}'"))
                else:
                    print(yellowify(result[0]))

            except sqlite3.OperationalError as e:
                print(redify(f"Error while reading schema of '{tbl}: {e}'"))

            return True
        
        case _:
            return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        db = sqlite3.connect(sys.argv[1])
        PROMPT = boldify(f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(sys.argv[1])} {blackify(">>")} ")
    else:
        db_name = input(blueify("Enter DB Path: "))
        PROMPT = boldify(f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(db_name)} {blackify(">>")} ")
        db = sqlite3.connect(db_name)

    while True:
        try:
            cmd = multiline_input(PROMPT)
            if not exec_builtin(cmd, db):
                exec_statement(cmd, db)

        except KeyboardInterrupt:
            print("^C")

        except EOFError:
            print(blueify("Bye"))
            break

    db.close()
