import smtplib
from email.message import EmailMessage

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import sqlite3
import joblib


from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

app.secret_key = "safeher_secret_key"

def send_alert_email():

    sender_email = "yourgmail@gmail.com"
    app_password = "YOUR_APP_PASSWORD"

    receiver_email = "receiver@gmail.com"

    msg = EmailMessage()

    msg["Subject"] = "🚨 SafeHer SOS Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        "Emergency SOS has been activated."
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            app_password
        )

        smtp.send_message(msg)

model = joblib.load("model/safety_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])

def predict():

    crime_rate = float(request.form["crime_rate"])
    crowd_density = float(request.form["crowd_density"])
    lighting = float(request.form["lighting"])
    time = float(request.form["time"])

    probability = model.predict_proba(
        [[crime_rate, crowd_density, lighting, time]]
    )[0][1]

    score = round(probability * 100, 2)


    if score >= 80:
        status = "SAFE"
        color = "green"

    elif score >= 50:
        status = "MODERATE RISK"
        color = "orange"

    else:
        status = "HIGH RISK"
        color = "red"

    if status == "SAFE":
         recommendation = "Area appears relatively safe."

    elif   status == "MODERATE RISK":

     recommendation = "Stay alert and avoid isolated routes."

    else:
     recommendation = "Avoid traveling alone and contact trusted people."


    return render_template(
    "index.html",
    score=score,
    status=status,
    color=color,
    recommendation=recommendation
)

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/services")
def services():
    return render_template("services.html")

from datetime import datetime

from datetime import datetime

@app.route("/sos")
def sos():

    current_time = str(datetime.now())

    conn = sqlite3.connect("safeher.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO alerts(time) VALUES(?)",
        (current_time,)
    )

    conn.commit()
    conn.close()

    send_alert_email()

    return render_template("sos.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


import sqlite3

@app.route("/save_contact", methods=["POST"])
def save_contact():

    name = request.form["name"]
    phone = request.form["phone"]

    conn = sqlite3.connect("safeher.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts(name,phone) VALUES(?,?)",
        (name, phone)
    )

    conn.commit()
    conn.close()

    return redirect("/contacts")

@app.route("/view_contacts")
def view_contacts():

    with open("contacts.txt", "r") as file:
        contacts = file.readlines()

    return render_template(
        "view_contacts.html",
        contacts=contacts
    )

@app.route("/history")
def history():

    with open("alerts.txt", "r") as file:
        alerts = file.readlines()

    return render_template(
        "history.html",
        alerts=alerts
    )

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
     return redirect("/login")

    conn = sqlite3.connect("safeher.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contacts")
    contacts_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    alerts_count = cursor.fetchone()[0]

    conn.close()

    labels = ["Contacts", "SOS Alerts"]
    values = [contacts_count, alerts_count]

    plt.figure(figsize=(5,4))
    plt.bar(labels, values)

    plt.title("SafeHer Analytics")
    plt.savefig("static/chart.png")
    plt.close()

    return render_template(
        "dashboard.html",
        contacts_count=contacts_count,
        alerts_count=alerts_count
    )


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    response = ""

    if request.method == "POST":

        message = request.form["message"].lower()

        if "night" in message:
            response = "Avoid isolated areas and share your live location with trusted contacts."

        elif "emergency" in message:
            response = "Use the SOS feature and contact emergency services immediately."

        elif "transport" in message:
            response = "Prefer well-lit areas and verified transport services."

        else:
            response = "Stay aware of your surroundings and keep emergency contacts accessible."

    return render_template(
        "chatbot.html",
        response=response
    )

@app.route("/route", methods=["GET","POST"])
def route():

    route_status = ""
    route_advice = ""

    if request.method == "POST":

        source = request.form["source"]
        destination = request.form["destination"]

        if len(source) + len(destination) > 20:

            route_status = "🟡 MODERATE RISK"

            route_advice = (
                "Travel during daytime and "
                "share your location with trusted contacts."
            )

        else:

            route_status = "🟢 SAFE"

            route_advice = (
                "Route appears relatively safe. "
                "Remain aware of surroundings."
            )

    return render_template(
        "route.html",
        route_status=route_status,
        route_advice=route_advice
    )

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("safeher.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("safeher.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

@app.route("/heatmap")
def heatmap():
    return render_template("heatmap.html")

@app.route("/nearby")
def nearby():
    return render_template("nearby.html")

@app.route("/voice")
def voice():
    return render_template("voice_sos.html")

if __name__ == "__main__":
    app.run(debug=True)