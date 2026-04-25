#!/usr/bin/env python
import readline
import sqlite3
import sys
import os

# Ansi Magic
redify = lambda x: f"\001\033[31m\002{x}\001\033[0m\002"
blueify = lambda x: f"\001\033[34m\002{x}\001\033[0m\002"
greenify = lambda x: f"\001\033[32m\002{x}\001\033[0m\002"
magentaify = lambda x: f"\001\033[35m\002{x}\001\033[0m\002"
yellowify = lambda x: f"\001\033[33m\002{x}\001\033[0m\002"
boldify = lambda x: f"\001\033[1m\002{x}\001\033[0m\002"


def multiline_input(prompt: str) -> str:
    buf = ""
    while True:
        if buf == "":
            line = input(prompt)
            if line.strip() == "":
                return ""
        else:
            line = input(f"{blueify("Continue")} {magentaify(">>")} ")

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
            print(magentaify("Void"))
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
        
        case [".tables"]:
            crs = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
            print(yellowify("Tables:"))
            hasTables = False
            for i in crs.fetchall():
                hasTables = True
                print(f"{blueify("->")} {greenify(i[0])}")

            if not hasTables:
                print(redify("No tables"))

            return True
        
        case [".schema"]:
            crs = db.execute("SELECT name, sql FROM sqlite_master")
            print(yellowify("Schema:"))
            hasTables = False
            for i in crs.fetchall():
                hasTables = True
                print(f"{blueify("->")} {greenify(i[0])}{magentaify(":")} {yellowify(i[1])}")
            
            if not hasTables:
                print(redify("No tables"))

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
        
        case [".sql", file_name]:
            try:
                with open(file_name) as f:
                    content = f.read()
                    db.executescript(content)
                    print(greenify(f"Successfully executed SQL Script {file_name}"))

            except sqlite3.OperationalError as e:
                print(redify(f"Error while executing SQL script: {e}"))
            
            except FileNotFoundError:
                print(redify(f"Could not find file: {file_name}"))

            return True

        
        case _:
            return False

def main():
    if len(sys.argv) > 1:
        db = sqlite3.connect(sys.argv[1])
        PROMPT = boldify(f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(sys.argv[1])} {magentaify(">>")} ")
    else:
        db_name = input(blueify("Enter DB Path: "))
        PROMPT = boldify(f"🐍 {greenify("PySQLSh")}{yellowify("@")}{blueify(db_name)} {magentaify(">>")} ")
        db = sqlite3.connect(db_name)

    histfile = os.path.join(os.path.expanduser("~"), ".pysqlsh_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        readline.write_history_file(histfile)
        print(greenify(f"Created history file at {histfile}."))
    finally:
        readline.set_history_length(1000)

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

        finally:
            readline.write_history_file(histfile)
        
    db.close()

if __name__ == "__main__":
    main()
