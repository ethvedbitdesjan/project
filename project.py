import os
from flask import Flask, request, render_template, redirect,flash,session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
import smtplib
import os
import csv
import math
def counting1():
    food = request.form.get("food")
    
    dish= request.form.get("dish")
    if request.form.get("amount1") is not None & dish is not None:
         amount1 = float(request.form.get("amount1"))
         num1=int(dish[-3:])
         main.total = main.total + (num1* amount1/100)
    if request.form.get("amount") is not None & food is not None:
        amount = float(request.form.get("amount"))
        num=int(food[-3:])
        main.total = main.total + (num* amount/100)
    
def main():
    main.total=0
    main.calories=0
    main.check=1
    main.username=""
    app.run()

    
app = Flask(__name__)
app.secret_key="bajabaja"
engine = create_engine("postgres://rwgezovhlswkpl:76b852320eeed7369c85e157e200560275201569c1920d13dd5d674840c1758b@ec2-52-70-15-120.compute-1.amazonaws.com:5432/da52lq56einar8")
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
    food_calories=db.execute("SELECT * FROM food_calories").fetchall()
    if main.check==1:
        session.pop("logged_in",None)
    if "logged_in" in session:
        string = "SELECT * FROM "
        string += main.username
        dish_calories = db.execute(string).fetchall()
        return render_template("count.html", food_calories=food_calories, dish_calories = dish_calories)
    else:
        return render_template("count.html", food_calories=food_calories)
@app.route("/count", methods=["POST"])
def count():
    counting1()
    return redirect("http://127.0.0.1:5000/")
@app.route("/sumup", methods=["POST"])
def sumup():
    counting1()
    return render_template("hello.html",total=main.total)
    main.total=0
@app.route("/new", methods=["POST"])
@login_required
def new_item():
    food_calories=db.execute("SELECT * FROM food_calories").fetchall()
    return render_template("newitem.html", food_calories=food_calories)
@app.route("/add", methods=["POST"])
@login_required
def add():
    name=request.form.get("name")
    calories = request.form.get("calories_amount")
    if name is not None & calories is not None:
        string="INSERT INTO "
        string +=main.username
        string+="(food_item, calories) VALUES (:name, :calories)"
        db.execute(string, {"name":name, "calories":calories})
        db.commit()
    return redirect("http://127.0.0.1:5000/")
@app.route("/countdish", methods=["POST"])
@login_required
def countdish():
    food = request.form.get("item")
    
    if request.form.get("amount") is not None & food is not None:
        num=int(food[-3:])
        amount=float(request.form.get("amount"))
        main.total = main.total+ (num * amount/100)
    return render_template("newitem.html")
@app.route("/add_dish",methods=["POST"])
@login_required
def add_dish():
    name=request.form.get("name")
    food = request.form.get("item")
    if request.form.get("amount") is not None & food is not None:
        num=int(food[-3:])
        amount=float(request.form.get("amount"))
        main.total = main.total+ (num * amount/100)
        string="INSERT INTO "
        string +=main.username
        string+="(food_item, calories) VALUES (:name, :calories)"
        db.execute(string, {"name":name, "calories":main.total})
        db.commit()
        flash("new dish added.")
    return redirect("http://127.0.0.1:5000/")
@app.route("/login.html", methods=["GET","POST"])
def login():
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
        main.check=0
        flash("you just logged in.")
        main.username=username
        return redirect("http://127.0.0.1:5000")
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("logged_in", None)
    flash("you just logged out.")
    return render_template("index.html")
@app.route("/register", methods=["POST"])
def register():
    if 'logged_in' in session:
        session.pop("logged_in", None)
    registered_user=None
    username = request.form.get("username")
    password = request.form.get("pass")
    if username is not None & password is not None:
      registered_user = db.execute("SELECT * FROM logins WHERE username = :username AND pass = :pass ", {"username":username, "pass":password}).fetchone()
      print(registered_user)
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
    else:
        flash("Invalid input")
    return render_template("login.html")
@app.route("/calculator")
def calculator():
    return render_template("calculator.html")
@app.route("/calculate", methods =["POST"])
def calculate():
    name = request.form.get("name")
    mass = request.form.get("mass")
    gender = request.form.get("gender")
    abdomen = request.form.get("abdomen")
    neck= request.form.get("neck")
    height = request.form.get("height")
    hip = request.form.get("hip")
    age = request.form.get("age")
    lifestyle = request.form.get("lifestyle")
    email = request.form.get("email")
    if not mass or  not gender or not height or not hip or not neck or not abdomen or not lifestyle or not name:
        return "failure"
    else:
        height = float(height)
        mass = float(mass)
        abdomen = float(abdomen)
        neck  =float(neck)
        hip = float(hip)
        age = float(age)
        if not email:
            emailenter =1
        bmi = mass / (height*height)
        if gender =="male":
            bmr = (10*mass)+(625* height) - (5*age) + 5
            body_fat_percentage = 495/((1.0324-(0.19077*(math.log10(abdomen - neck))) - (0.15456*(math.log10(height)))) -450)
        else:
            body_fat_percentage = 495/(1.29579-(0.35004*(math.log10(abdomen + hip - neck))) + (0.22100*(math.log10(height*100)))) - 450
            bmr = (10*mass)+(625* height) - (5*age) -161
    
        
        if lifestyle =="sedentary":
            calorie = bmr*1.2
        elif lifestyle == "light":
            calorie = bmr*1.375
        elif lifestyle == "moderate":
            calorie = bmr*1.55
        else:
            calorie = bmr*1.725
        lean_mass = mass - (mass*body_fat_percentage/100)
        bmi = round(bmi,2)
        bmr = round(bmr,2)
        lean_mass = round(lean_mass,2)
        body_fat_percentage = round(body_fat_percentage,2)
        calorie = round(calorie,2)
        message = "your bmr is " + str(bmr) + " and your daily requirement of calories is " + str(calorie) 
        message = message + "yoour body fat percentage is " + str(body_fat_percentage)
       
        
        if email !="":
            print(email+"hi")
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("ved6734@gmail.com","diokdmgnfmpyjvxk")
            server.sendmail("ved6734@gmail.com",email, message)
        file = open("registered.csv", "a")
        writer = csv.writer(file)
        writer.writerow((name, age, lifestyle, bmi, bmr, lean_mass,calorie, body_fat_percentage))
        file.close()
        return render_template("support.html", bmi = bmi,bmr=bmr,lean_mass=lean_mass,calorie=calorie, body_fat_percentage=body_fat_percentage)
@app.route("/message", methods=["GET", "POST"])
def message():
    feedback0 = request.form.get("feedback")
    if request.form.get("valuable_name") is not None:
        name = request.form.get("valuable_name")
        feedback0+="sent by" + name
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("ved6734@gmail.com","diokdmgnfmpyjvxk")
        server.sendmail("ved6734@gmail.com","ved6734@gmail.com", feedback0)
    db.execute("INSERT INTO feedback(name, feedback) VALUES (:name, :feedback)", {"name":name, "feedback":feedback0})
    return redirect("http://127.0.0.1:5000/")
if __name__== '__main__':
    main()