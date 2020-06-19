import os
from flask import Flask, request, render_template, redirect,flash,session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
import smtplib
import os
import csv
import math
total1 =0
calories1=0
check1=1
username1=""
def counting1():
    global total1, calories1, check1, username1
    stringnone=None
    food =None
    stringnone =request.form.get("amount")
    food = request.form.get("food")
    if not stringnone or not food:
        flash("invalid input")
    else:
        amount = float(request.form.get("amount"))
        num=int(food[-3:])
        total1 = total1 + (num* amount/100)
   
    
def main():
   app.run()    
app = Flask(__name__)
app.secret_key="bajabaja"
engine = create_engine("postgres://ulifhsfotoxlau:8d5be9febece7cf7019f40c8063081a88c2a5ef866a6cee5fcf59b0e04bc9713@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dbguileu0eavj8")
db = scoped_session(sessionmaker(bind=engine))

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return render_template("login.html")
    return wrap
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/count.html")
def count_calories():
    global check1, calories1, total1
    food_calories=db.execute("SELECT * FROM food_calories").fetchall()
    if check1==1:
        session.pop("logged_in",None)
    if "logged_in" in session:
        string = "SELECT * FROM "
        string += username1
        dish_calories = db.execute(string).fetchall()
        return render_template("count.html", food_calories=food_calories, dish_calories = dish_calories)
    else:
        return render_template("count.html", food_calories=food_calories)
@app.route("/count", methods=["POST"])
def count():
    counting1()
    food_calories=db.execute("SELECT * FROM food_calories").fetchall()
    if "logged_in" in session:
        string = "SELECT * FROM "
        string += username1
        dish_calories = db.execute(string).fetchall()
        return render_template("count.html", food_calories=food_calories, dish_calories = dish_calories)
    else:
        return render_template("count.html", food_calories=food_calories)
@app.route("/sumup", methods=["POST"])
def sumup():
    global total1, calories1, check1, username1
    counting1()
    return render_template("hello.html",total=total1)
    total1=0

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    global username1, total1, check1, calories1
    if request.method =="GET":
         food_calories=db.execute("SELECT * FROM food_calories").fetchall()
         return render_template("newitem.html", food_calories=food_calories)
    elif request.method=="POST":
     global username1, total1, calories1, check1
     name=request.form.get("name")
     calories = request.form.get("calories_amount")
     if not name or not calories:
        flash("you put invlid data.")
     else:
        string="INSERT INTO "
        string +=username1
        string+="(food_item, calories) VALUES (:name, :calories)"
        db.execute(string, {"name":name, "calories":calories})
        db.commit()
        flash("item added.")
     return redirect("https://projectcalories7.herokuapp.com/add")
@app.route("/countdish", methods=["POST"])
@login_required
def countdish():
    food = request.form.get("item")
    global total1, calories1, username1, check1
    if request.form.get("amount")!=0 & food !="none":
        num=int(food[-3:])
        amount=float(request.form.get("amount"))
        total1 = total1+ (num * amount/100)
    return redirect("https://projectcalories7.herokuapp.com/add")
@app.route("/add_dish",methods=["POST"])
@login_required
def add_dish():
    global total1, calories1, username1, check1
    print(username1)
    name=None
    food=None
    stringnone=None
    stringnone =request.form.get("amount")
    name=request.form.get("name")
    food = request.form.get("item")
    if not stringnone or not food:
        num=int(food[-3:])
        amount=float(request.form.get("amount"))
        total1 = total1+ (num * amount/100)
        string="INSERT INTO "
        string +=username1
        string+="(food_item, calories) VALUES (:name, :calories)"
        db.execute(string, {"name":name, "calories":total1})
        db.commit()
        flash("new dish added.")
    return redirect("https://projectcalories7.herokuapp.com/")
@app.route("/login.html", methods=["GET","POST"])
def login():
    global username1, total1, check1, calories1
    if request.method=="GET":
        return render_template("login.html")
    else:
     username="h"
     password="pass"
     username = request.form.get("username")
     password = request.form.get("pass")
     registered_user=None
     registered_user = db.execute("SELECT * FROM logins WHERE username = :username AND pass = :pass", {"username": username, "pass": password}).fetchone()
     db.commit()
     if registered_user is None:
        flash("invalid credentials")
        return render_template("login.html")
     else:
        session['logged_in']=True
        check1=0
        flash("you just logged in.")
        username1=username
        return redirect("https://projectcalories7.herokuapp.com/")
@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("you just logged out.")
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def register():
    global username1, total1, check1, calories1
    if 'logged_in' in session:
        session.pop("logged_in", None)
    registered_user=None
    username = request.form.get("username")
    password = request.form.get("pass")
   
    registered_user = db.execute("SELECT * FROM logins WHERE username = :username AND pass = :pass ", {"username":username, "pass":password}).fetchone()
      
    if registered_user is None:
       db.execute("INSERT INTO logins(username, pass) VALUES (:username, :pass)",{"username":username, "pass":password})
       t_name_tbl = username
       s = ""
       s += "CREATE TABLE " + t_name_tbl + "("
       s += " id serial NOT NULL,"
       s += "food_item VARCHAR NOT NULL,"
       s += "calories INTEGER NOT NULL"
       s += " ); "
       db.execute(s)
       db.commit()
       flash("you have registered. please login.")
    
    else:
       flash("user already registered!")
       registered_user=None
   
    return render_template("login.html")
@app.route("/calculator")
def calculator():
    return render_template("calculator.html")
@app.route("/bdf", methods=["POST"])
def bdf():
    name = request.form.get("name")
    mass = request.form.get("mass")
    gender = request.form.get("gender")
    abdomen = request.form.get("abdomen")
    neck= request.form.get("neck")
    height = request.form.get("height")
    hip = request.form.get("hip")
   
    email = request.form.get("email")
    if not height or not neck or not abdomen or not mass:
        flash("invalid input")
        return render_template("error.html", msg="failure! Required data was not provided.")
    else:
        height = float(height)
        mass = float(mass)
        abdomen = float(abdomen)
        neck  =float(neck)
        hip = float(hip)
        height= height*100
        emailenter=0
        if not email:
            emailenter =1
        if gender =="male":
            body_fat_percentage = 495/(1.0324 - (0.19077 * (math.log10(87 - 51))) + (0.15456*(math.log10(163))))-450 
        else:
            body_fat_percentage=495/(1.29579-(0.35004*(math.log10(87 + 83 - 51))) + (0.22100*(math.log10(163)))) - 450
        lean_mass = mass - (mass*body_fat_percentage/100)
        lean_mass = round(lean_mass,2)
        body_fat_percentage = round(body_fat_percentage,2)
        message = "yoour body fat percentage is " + str(body_fat_percentage)
        message+="your lean mass is " + str(lean_mass)
        if emailenter!=1:
            print(email+"hi")
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("ved6734@gmail.com","diokdmgnfmpyjvxk")
            server.sendmail("ved6734@gmail.com",email, message)
        return render_template("support.html", lean_mass=lean_mass, body_fat_percentage=body_fat_percentage)
@app.route("/calculate", methods =["POST"])
def calculate():
    name = request.form.get("name")
    mass = request.form.get("mass")
    gender = request.form.get("gender")
    height = request.form.get("height")
    age = request.form.get("age")
    lifestyle = request.form.get("lifestyle")
    email = request.form.get("email")
    if not mass or  not gender or not height or not lifestyle:
        return render_template("error.html",msg ="failure. Required data was not provided")
    else:
        height = float(height)
        mass = float(mass)
        age = float(age)
        emailenter=0
        if not email:
            emailenter =1
        bmi = mass / (height*height)
        if gender =="male":
            bmr = (10*mass)+(625* height) - (5*age) + 5
            
        else:
            
            bmr = (10*mass)+(625* height) - (5*age) -161
    
        
        if lifestyle =="sedentary":
            calorie = bmr*1.2
        elif lifestyle == "light":
            calorie = bmr*1.375
        elif lifestyle == "moderate":
            calorie = bmr*1.55
        else:
            calorie = bmr*1.725
        
        bmi = round(bmi,2)
        bmr = round(bmr,2)
        
        calorie = round(calorie,2)
        message = "your bmr is " + str(bmr) +", your bmi is " + str(bmi) + " and your daily requirement of calories is " + str(calorie) 
      
        
        if emailenter !=1:
            print(email+"hi")
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("ved6734@gmail.com","diokdmgnfmpyjvxk")
            server.sendmail("ved6734@gmail.com",email, message)
        file = open("registered.csv", "a")
        writer = csv.writer(file)
        writer.writerow((name, age, lifestyle, bmi, bmr,calorie))
        file.close()
        return render_template("support.html", bmi = bmi,bmr=bmr,calorie=calorie)
@app.route('/diet_cal', methods=["GET" , "POST" ])
def diet_plan():
    if request.method=="GET":
        return render_template("diet_plan.html")
    else:
        req_cal = float(request.form.get("req_calories"))
        reduce_cal = float(request.form.get("reduce_cal"))
        req_cal = req_cal - reduce_cal
        carb = (0.4 * req_cal)/4
        protein = (0.3 * req_cal)/4
        fat = (0.3 * req_cal)/9
        return render_template("diet.html", fat=fat, protein=protein, carb=carb)
@app.route("/message", methods=["GET", "POST"])
def message():
    stringnone = None
    stringnone =request.form.get("valuable_name")
    feedback0 = request.form.get("feedback")
    if stringnone is not None:
        name = request.form.get("valuable_name")
        feedback0+="sent by" + name
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("ved6734@gmail.com","diokdmgnfmpyjvxk")
        server.sendmail("ved6734@gmail.com","ved6734@gmail.com", feedback0)
    db.execute("INSERT INTO feedback(name, feedback) VALUES (:name, :feedback)", {"name":name, "feedback":feedback0})
    return redirect("https://projectcalories7.herokuapp.com/")
if __name__== '__main__':
    main()
