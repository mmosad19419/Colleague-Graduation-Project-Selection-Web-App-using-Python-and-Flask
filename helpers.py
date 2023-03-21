import sqlite3
from pathlib import Path
import os
from cs50 import SQL
import csv
from functools import wraps
from flask import redirect, session

#configure database
db = SQL("sqlite:///students.db")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("student_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def alogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/admin/login")
        return f(*args, **kwargs)
    return decorated_function


def read_data (folderpath, database):
    #connect our database
    con = sqlite3.connect(database)
    cur = con.cursor()

    #go to the project dir
    files = Path(folderpath)
    for file in files.iterdir():
        if file.name.endswith('csv'):
            data = file

    if data == None:
        return False

    cur.execute("DELETE FROM students WHERE id >0;")
    cur.execute("DELETE FROM projects WHERE id >0;")
    with open(data , "r") as data:
        reader = csv.reader(data)
        next(reader)

        for row in reader:
            fcolumn = row[0]
            scolumn = row[1]
            tcolumn = row[2]

            #insert our data into database
            cur.execute("INSERT INTO students (acamail, name, score) VALUES (?, ?, ?)", (fcolumn,scolumn,tcolumn))

    con.commit()
    con.close()
    return True


def clear_dir(dirpath):
    #go to the project dir
    files = Path(dirpath)
    for file in files.iterdir():
        if file.name.endswith('csv'):
            os.remove(file)


#admin control variable
admin_control = 1

#declare projects
projects = ["Structural Engineering", "Reinforced Concrete Design",
            "Sanitary Engineering", "Hrydrolics Engineering", "Soil Mechanics and Foundation Engineering",
            "Highways and Traffic Engineering", "Survey Engineering"]

nprojects = len(projects)
