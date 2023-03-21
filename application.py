import os
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from helpers import clear_dir, login_required, alogin_required, db, read_data, admin_control, nprojects
from werkzeug.utils import secure_filename
import math


app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

Session(app)


def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1] 
    
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


#Routes Controls
#register route
@app.route("/register", methods=["GET", "POST"])
def register():
    #control get request
    if request.method == "GET":
        return render_template("register.html")
    
    #control post request
    if request.method == "POST":
        #Check if the result is calculated before or not
        final_selected = db.execute("SELECT COUNT(id) FROM students WHERE final != 'NULL'")[0]["COUNT(id)"]
        #Check
        if final_selected != 0:
            return render_template("apology.html", message ="Registeration is closed", code = "400", route="register")

        #insure data is entered and canocalize it
        # Ensure mail was submitted
        mail = request.form.get("mail").strip().lower()
        if not mail:
            return render_template("apology.html", message ="must provide mail", code = "400", route="register")
    
        # Ensure password was submitted
        passward = request.form.get("password").strip().lower()
        if not passward:
            return render_template("apology.html", message ="must provide password", code = "400", route="register")
    
        # Ensure password again was submitted
        confirmation = request.form.get("confirmation").strip().lower()
        if not confirmation:
            return render_template("apology.html", message ="must provide password confirmation", code = "400", route="register")

        # Ensure that confirmation is the same as passward
        if confirmation != passward:
            return render_template("apology.html", message ="password and confirmation not match", code = "400", route="register")

        # Query database for mail
        rows = db.execute("SELECT * FROM students WHERE acamail = ?", mail)
    
        # Ensure mail exists in database
        if len(rows)!= 1:
            return render_template("apology.html", message ="invalid, academic mail is not valid", code = "400", route="register")

        elif len(rows) == 1:
            # save the user passward
            db.execute("UPDATE students SET pass= ? WHERE acamail= ?", passward, mail)
        
        #after register user redirect to login
        return redirect("/login")


#login route
@app.route("/login", methods = ["GET", "POST"])
def login():
    #control get request
    if request.method == "GET":
            return render_template("login.html")
    
    #control post request
    if request.method == "POST":
        #insure data is entered and canocalize it
        # Ensure mail is submitted
        mail = request.form.get("mail").strip().lower()
        if not mail:
            return render_template("apology.html", message ="must provide mail", code = "400", route="login")
        
        # Ensure password was submitted
        passward = request.form.get("password").strip().lower()
        if not passward:
            return render_template("apology.html", message ="must provide passward", code = "400", route="login")

        #student log in process
        rows = db.execute("SELECT * FROM students WHERE acamail = ?", mail)
        # check the mail
        if len(rows)!= 1:
            return render_template("apology.html", message ="invalid, academic mail is not valid", code = "400", route="login")
            
        # check registeration
        elif rows[0]['pass'] == None:
            return render_template("apology.html", message ="invalid, You have to register first. Go to 'register' tab", code = "400", route="login")

        # if mail valid, check passward
        elif len(rows) == 1:
            pass_check = db.execute("SELECT * FROM students WHERE pass = ? AND acamail = ?", passward, mail)
          
            if len(pass_check)!= 1:
                return render_template("apology.html", message ="invalid, passward", code = "400", route="login")
        
        #log the student
        # Remember which student has logged in
        session["student_id"] = rows[0]["id"]
        
        #redirect the student to the home page
        return redirect("/")

#index route
@app.route("/")
@login_required
def home():
    student_id = session["student_id"]
    student = db.execute("SELECT * FROM students WHERE id = ?", student_id)[0]

    #check if the user have submit choices before or not
    projects = db.execute("SELECT projects FROM projects WHERE id_projects = ?", student_id)
    
    # if the student submit choices present them
    if len(projects) != 0:
        return render_template("index.html", student=student, projects=projects)

    # if the student did not submit choices
    return render_template("index.html", student=student, projects="none")


# select route
@app.route("/select", methods=["POST", "GET"])
@login_required
def select():
    # if request.method = get
    if request.method == "GET":
        # selection required data
        projects = ["Structural Engineering", "Reinforced Concrete Design",
            "Sanitary Engineering", "Hrydrolics Engineering", "Soil Mechanics and Foundation Engineering",
            "Highways and Traffic Engineering", "Survey Engineering"]

        nprojects = range(1, len(projects)+1)

        return render_template("select.html", projects=projects, nprojects = nprojects)
    
    # control post request
    if request.method == "POST":
        #Check if the result is calculated before or not
        final_selected = db.execute("SELECT COUNT(id) FROM students WHERE final != 'NULL'")[0]["COUNT(id)"]
        #Check
        if final_selected != 0:
            return render_template("apology.html", message ="Selection is closed", code = "400", route="select")
            
        student_id = session["student_id"]

        #required data
        projects = ["Structural Engineering", "Reinforced Concrete Design",
            "Sanitary Engineering", "Hrydrolics Engineering", "Soil Mechanics and Foundation Engineering",
            "Highways and Traffic Engineering", "Survey Engineering"]


        #check if the user have submit choices before or not
        sprojects = db.execute("SELECT * FROM projects WHERE id_projects = ?", student_id)
        
        if len(sprojects) != 0 :
            #then the student submmited before so render error messagr 
            return render_template("apology.html", message ="invalid, you have submited chocies before, if you want to edit your submissions go to 'Edit projects Selection' tab", code = "400", route="select")
        
        elif len(sprojects) == 0 :
            #save student choices into database
            # get form data and check it
            nprojects = range(1, len(projects)+1)
            for i in nprojects:
                project = request.form.get(f"project{i}")
                if (not project) or (project not in projects):
                    return render_template("apology.html", message ="invalid, Missing or wrong choice", code = "400", route="select")
                else:
                    db.execute("INSERT INTO projects (id_projects, projects) VALUES(?, ?)", student_id, project)
        #redirect user to home page
        return redirect("/")


#edit selection route
@app.route("/edit", methods=["POST", "GET"])
@login_required
def edit():
     # if request.method = get
    if request.method == "GET":
        # selection required data
        projects = ["Structural Engineering", "Reinforced Concrete Design",
            "Sanitary Engineering", "Hrydrolics Engineering", "Soil Mechanics and Foundation Engineering",
            "Highways and Traffic Engineering", "Survey Engineering"]

        nprojects = range(1, len(projects)+1)

        return render_template("edit.html", projects=projects, nprojects = nprojects)
    
    # control post request
    if request.method == "POST":
        #Check if the result is calculated before or not
        final_selected = db.execute("SELECT COUNT(id) FROM students WHERE final != 'NULL'")[0]["COUNT(id)"]
        #Check
        if final_selected != 0:
            return render_template("apology.html", message ="Selection is closed", code = "400", route="edit")
            
        student_id = session["student_id"]

        #required data
        projects = ["Structural Engineering", "Reinforced Concrete Design",
            "Sanitary Engineering", "Hrydrolics Engineering", "Soil Mechanics and Foundation Engineering",
            "Highways and Traffic Engineering", "Survey Engineering"]
        
        #check if the student select projects before
        selected = db.execute("SELECT COUNT(projects) FROM projects WHERE id_projects = ?", student_id)[0]["COUNT(projects)"]
                
        if selected == 0:
            return render_template("apology.html", message ="You did not select any projects yet!, Select project first", code = "400", route="select")
        
        else:
            db.execute("DELETE FROM projects WHERE id_projects = ?", student_id)

            #save student choices into database
            # get form data and check it
            nprojects = range(1, len(projects)+1)
            for i in nprojects:
                project = request.form.get(f"project{i}")
                if (not project) or (project not in projects):
                    return render_template("apology.html", message ="invalid, Missing or wrong choice", code = "400", route="edit")
                else:
                    db.execute("INSERT INTO projects (id_projects, projects) VALUES(?, ?)", student_id, project)
                #redirect user to home page
            return redirect("/")


# result view route
@app.route("/result")
@login_required
def student_result():
    student_id = session["student_id"]
    student = db.execute("SELECT final FROM students WHERE id = ?", student_id)[0]

    return render_template("result.html", student=student)


# logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# _________________________________________________________admin controls________________________________________________

# admin main route
@app.route("/admin/", methods = ["GET", "POST"])
@alogin_required
def main():
    if request.method == "GET":
        # query data from db
        #total student number
        tstudents = len(db.execute("SELECT * FROM students"))
        #total regidtered students
        registered = len(db.execute("SELECT * FROM students WHERE pass != 'NULL'"))
        #total students filled selections
        fstudents = db.execute("SELECT COUNT(DISTINCT id_projects) from projects")[0]["COUNT(DISTINCT id_projects)"]

        admin_control = 0

        return render_template("aindex.html", tstudents=tstudents, registered=registered, fstudents=fstudents)




#login route
@app.route("/admin/login", methods = ["GET", "POST"])
def alogin():
    if request.method == "GET":
            return render_template("alogin.html")
    
    if request.method == "POST":
        #insure data is entered and canocalize it
        # Ensure mail is submitted
        mail = request.form.get("mail").strip().lower()
        if not mail:
            return render_template("aapology.html", message ="must provide mail", code = "400", route="login")
        
        # Ensure password was submitted
        passward = request.form.get("password").strip().lower()
        if not passward:
            return render_template("aapology.html", message ="must provide passward", code = "400", route="login")

        #admin log in process
        adminrow = db.execute("SELECT * FROM admin WHERE mail = ?", mail)
        # check the mail
        if len(adminrow)!= 1:
            return render_template("aapology.html", message ="invalid, admin mail is not valid", code = "400", route="login")
                
        # if mail valid, check passward
        elif len(adminrow) == 1:
                pass_check = db.execute("SELECT * FROM admin WHERE pass = ? AND mail = ?", passward, mail)
           
                if len(pass_check)!= 1:
                    return render_template("aapology.html", message ="invalid, passward", code = "400", route="login")
                
        #log the admin
        session["admin_id"] = adminrow[0]["id"]
            
        #redirect the admin to the control page page
        return redirect("/admin")




#upload route
@app.route("/admin/upload", methods = ["GET", "POST"])
@alogin_required
def upload():
    if request.method == "GET":
        return render_template("aupload.html")
    
    if request.method == "POST":
        if request.files:
            csv = request.files["csv"]
             
            if csv.filename == "":
                return render_template("aapology.html", message ="must provide a file with a proper filename", code = "400", route="upload")

            if not allowed_file(csv.filename):
                return render_template("aapology.html", message ="must provide a file with a CSV file format", code = "400", route="upload")
            
            else:
                filename = secure_filename(csv.filename)
                #remove all previous files
                clear_dir(app.config["FILES_UPLOAD"])
                #save new file
                csv.save(os.path.join(app.config["FILES_UPLOAD"], filename))
                #Read data to the data base
                if read_data(app.config["FILES_UPLOAD"], "students.db"):
                    return redirect("/admin/upload")
                else:
                    return render_template("aapology.html", message ="must provide a Valid file with a CSV file format", code = "400", route="upload")
                    
        return redirect("/admin/upload")



#result route control
@app.route("/admin/result", methods = ["GET" , "POST"])
@alogin_required
def result():
    if request.method == "GET":
        return render_template("aresult.html")
    
    if request.method == "POST":
        students = db.execute("SELECT * FROM students WHERE pass != 'NULL' ORDER BY score")
        project_num = len(students) / nprojects
        # to handle if the divison result not integer
        project_cap = math.ceil(project_num)
        
        #Check if the result is calculated before or not
        final_selected = db.execute("SELECT COUNT(id) FROM students WHERE final != 'NULL'")[0]["COUNT(id)"]
        #Check
        if final_selected != 0:
            return render_template("aapology.html", message ="Result Calculated Before", code = "400", route="result")
        else:
            for student in students:
                selections = db.execute("SELECT projects FROM projects WHERE id_projects = ? AND projects != 'NULL'", student["id"])
            
                for selection in selections: 
                    pnumber = db.execute("SELECT COUNT(id) FROM students WHERE final = ?", selection["projects"])[0]["COUNT(id)"]
    
                    if pnumber < project_cap:
                        db.execute("UPDATE students SET final = ? WHERE id = ?", selection["projects"], student["id"])
                        break
        

        return render_template("acresult.html", message ="Student results are ready", route="result")


        
#admin logout
@app.route("/admin/logout")
@alogin_required
def alogout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/admin")