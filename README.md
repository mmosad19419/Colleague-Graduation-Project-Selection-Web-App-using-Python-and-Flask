# Final Project Selection
## Video Demo:  [URL](https://youtu.be/ZAr-5f161TE)
## Description: 

#### This is **CS50 final projects**
###### The problem that inspire the project was that the graduation project selection process at college we have a very tedious selection process which staff lists multiple projects to choose from and we fill paper with our choices and manually the staff assign each on to the project based on the grades, this process causes a lot of issues and we may reassign the projects multiple times, the project was a collaberation with 2 of my colleagues, 

###### my project is a web application that allows both students and teaching staff to make the process of student graduation project selection process as easy as possible for the students and easy to prepare for the teaching staff.

Let us start with the functionality of the web app

#### Teaching staff (admin)
##### Home page
I call them in my implementation the admin the one who has control of the data of the web app so the admin has three tabs first one is Home Page his is the admin can see how many students are allowed to register, registered, and students who have selected their projects.

##### Upload student data
the tab admin can upload student's data through a CSV file that has the academic mail and password and the score of each student

##### Calculate result
tab the admin can click a button to let the web app do the selection process when the admin clicks on this button the selection algorithm will be applied and each student will get its result and the registration and selection process will be closed for all students

#### Students
here students can register using their Academic mail and set a password to their account and then enter and select their projects also can edit their selection until the admin determines when to calculate the result and then the students can enter and view their selected Final project

##### Home page
Home page for viewing student's data academic mail, name, score, and selected project if the student has selected his projects

##### Selection page
On this page, students can arrange their preferred projects with some instructions viewed and presented on the page.

##### Edit Selection page
On this page, students can edit the arrangement of their preferred projects with some instructions viewed and presented on the page.

##### Result page
 On this page student view and know their final year project after the selection process.

#### How we build this app
I used the Flask-Python framework to implement this project and control the app through routes for students and admin, and I used a separate configuration file and a **helpers.py** File for helper functions to use inside my app, a (**read_data**) function to read data from a CSV file to a certain database, the database configuration and (**login_required and alogin_required**) to ensure the user logged in before. and a (clear_dir) function to clear the directory used to store uploaded files from any file uploaded before with all these components combined I build this web app with the functionality I presented before.

#### database Design
The database is a very simple one-to-many relational database with two tables.
Student table to store students' data columns >id, academic mail, name, password, and score.
 
projects table referencing students' table on the id column to store projects of each student columns > id, id_projects, and projects.









