# PySQLSh
A shell for interacting with SQLite databases written in Python

## How do I use it?
### Cloning and launching/installing
To clone this repository and launch the python script:

```bash
git clone https://github.com/Moritisimor/PySQLSh
cd PySQLSh
python pysqlsh.py
```

To install the script, you can use pip:

```bash
git clone https://github.com/Moritisimor/PySQLSh
cd PySQLSh
pip install .
pyqsqlsh
```

(Note: you should use pipx for this if you want to install it globally without using a virtual environment)

You should then be prompted to enter the path to a SQLite database. 

If you only want to look around, you can just type ```:memory:``` to use an in-memory database.

Instead of entering the path to the database each time, you can just pass it as a CLI argument like this:

```bash
python pysqlsh.py path/to/database
```

What's important to note is that PySQLSh uses ; to determine when input is done.

### Interacting with databases
You can simply execute SQL statements with this shell. 

For example, to create a table:

![Table Creation](screenshots/CreateTableScreenshot.png)

Insert some data:

![Data Insertion](screenshots/InsertDataScreenshot.png)

And then query it:

![Data Querying](screenshots/QueryScreenshot.png)

### Builtins
PySQLSh also features a few builtins.

To see the schema of all tables:

![Schema of all Tables](screenshots/ViewAllSchemasScreenshot.png)

To see the schema of a particular table:

![Schema of one Table](screenshots/ViewSchemaScreenshot.png)

To see all tables:

![All Tables](screenshots/ViewTablesScreenshot.png)

To execute a SQL script:

![Executing a SQL script](screenshots/ExecuteScriptScreenshot.png)

PySQLSh also has some other builtins that are less spectacular.

```.exit``` to exit the database. Alternatively, you can just enter Ctrl + D with an empty prompt.

```.clear``` to clear the screen.

