import os
import re
import random
import pytz

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from cs50 import SQL
from datetime import datetime, timedelta
from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///chat.db")

#   a sample database with few profiles
#   db = SQL("sqlite:///sample.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def get_user_info(user_id):
    user = {}
    username = db.execute("SELECT username FROM people WHERE id = ?", user_id)[0]["username"]
    user["username"] = username
    dp_src = db.execute("SELECT dp_src FROM account WHERE person_id = ?", user_id)[0]["dp_src"]
    file_path = f"../static/media/profile_pictures/{dp_src}"
    friends = db.execute("""SELECT id, username
        FROM people
        WHERE id IN (
            SELECT
            CASE
                WHEN friend_id = ? THEN person_id
                ELSE friend_id
            END AS friend_id
        FROM friends
        WHERE person_id = ? OR friend_id = ?)""", user_id, user_id, user_id)
    people = db.execute("SELECT id, username FROM people")

    for friend in friends:
        dp = db.execute("SELECT dp_src FROM account WHERE person_id = ?", friend["id"])
        dp_src = dp[0]["dp_src"]
        friend["dp_src"] = "../static/media/profile_pictures/" + dp_src

        last_chat = db.execute("SELECT sender_id, receiver_id, message, status, MAX(timestamp) AS timestamp FROM conversations WHERE (sender_id = ? AND receiver_id = ?) OR (receiver_id = ? AND sender_id = ?) GROUP BY sender_id ORDER BY timestamp DESC", user_id, friend["id"], user_id, friend["id"])

        if last_chat:
            if int(last_chat[0]["sender_id"]) == user_id:
                friend["sent"] = True
                friend["status_tick"] = f"../static/media/icons/{last_chat[0]["status"]}.png"
            friend["last_message"] = last_chat[0]["message"]

            message = get_message(last_chat[0]["timestamp"])
            if message == "TODAY":
                friend["last_time"] = convert_to_ist(last_chat[0]["timestamp"])
            else:
                friend["last_time"] = message.capitalize()

            friend["timestamp"] = last_chat[0]["timestamp"]
        else:
            friend["no_message"] = "Start a new conversation"
            friend["timestamp"] = "0000-00-00 00:00:00"

    sorted_friends = sorted(friends, key=lambda x: x['timestamp'], reverse=True)

    request_noti = db.execute("SELECT COUNT(*) AS count FROM friend_request WHERE receiver_id = ? AND status = 'sent'", user_id)
    if request_noti:
        user["request_noti"] = request_noti[0]["count"]
    return {"user": user, "dp_src": file_path, "people": people, "friends": sorted_friends}

def show_requests():
    user_id = session["user_id"]
    requests = db.execute("SELECT receiver_id, sender_id, status, timestamp FROM friend_request WHERE sender_id = ? OR receiver_id = ? ORDER BY timestamp DESC", user_id, user_id)

    for req in requests:
        if req["receiver_id"] == user_id:
            req["sender_name"] = db.execute("SELECT username FROM people WHERE id = ?", req["sender_id"])[0]["username"]
        elif req["sender_id"] == user_id:
            req["receiver_name"] = db.execute("SELECT username FROM people WHERE id = ?", req["receiver_id"])[0]["username"]

    return requests

def convert_to_ist(timestamp):
    dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    ist = pytz.timezone('Asia/Kolkata')
    return dt_object.replace(tzinfo=pytz.utc).astimezone(ist).strftime("%H:%M")

def get_message(timestamp):
    dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    ist = pytz.timezone('Asia/Kolkata')
    dt_object_ist = dt_object.replace(tzinfo=pytz.utc).astimezone(ist)

    date = dt_object_ist.strftime("%Y-%m-%d")

    today_ist = datetime.now(ist).date()
    yesterday_ist = today_ist - timedelta(days=1)

    if date == today_ist.strftime("%Y-%m-%d"):
        message = "TODAY"
    elif date.lower() == yesterday_ist.strftime("%Y-%m-%d"):
        message = "YESTERDAY"
    elif dt_object_ist.date() >= today_ist - timedelta(days=(today_ist.weekday() + 1)):
        message = dt_object_ist.strftime("%A").upper()
    else:
        message = dt_object_ist.strftime("%d/%m/%Y")

    return message

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    info = get_user_info(user_id)
    user = info["user"]
    file_path = info["dp_src"]
    friends = info["friends"]
    new_chats = db.execute("SELECT sender_id, COUNT(message) AS count_noti, timestamp FROM conversations WHERE receiver_id = ? AND (status = 'sent' OR status = 'reached') GROUP BY sender_id", user_id)

    for friend in friends:
        notification = [chat["count_noti"] for chat in new_chats if chat["sender_id"] == friend["id"]]
        if notification:
            friend["notification"] = notification[0]
        db.execute("UPDATE conversations SET status = 'reached' WHERE receiver_id = ? and status = 'sent'", user_id)
    sorted_friends = sorted(friends, key=lambda x: x['timestamp'], reverse=True)
    return render_template("home.html", user=user, dp_src=file_path, friends=sorted_friends)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")
        elif not password:
            return apology("must provide password")

        rows = db.execute("SELECT * FROM people WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("missing username!")
        elif not password:
            return apology("missing password!")
        elif not confirmation:
            return apology("missing confirmation!")

        rows = db.execute("SELECT * FROM people WHERE username = ?", username)

        if rows:
            return apology("username already taken!")
        elif password != confirmation:
            return apology("passwords don't match!")

        hash = generate_password_hash(password)

        dp_folder = "static/media/profile_pictures"
        dp_files = os.listdir(dp_folder)
        random.shuffle(dp_files)

        def get_next_dp():
            if not dp_files:
                random.shuffle(dp_files)
            selected_dp = dp_files.pop()
            return selected_dp
        random_dp = get_next_dp()

        user_id = db.execute("INSERT INTO people (username, hash) VALUES (?, ?)", username, hash)
        session["user_id"] = user_id
        db.execute("INSERT INTO account (person_id, dp_src) VALUES (?, ?)", user_id, random_dp)


        flash("Registered! Welcome to Chat50")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/addFriend", methods=["GET", "POST"])
@login_required
def addFriend():
    if request.method == "POST":
        friend = request.form.get("addFriend")

        user_id = session["user_id"]
        info=get_user_info(user_id)
        user = info["user"]
        file_path = info["dp_src"]
        people = info["people"]
        friends = info["friends"]

        if not friend:
            return render_template("addFriend.html", user=user, dp_src=file_path, friends=friends, response="USER DOES NOT EXIST")
        elif friend not in [person["username"] for person in people]:
            return render_template("addFriend.html", user=user, dp_src=file_path, friends=friends, response="USER DOES NOT EXIST")

        friend_id = db.execute("SELECT id FROM people WHERE username = ?", friend)[0]["id"]
        requests_received = db.execute("SELECT sender_id FROM friend_request WHERE receiver_id = ? AND status = 'sent'", user_id)
        requests_sent = db.execute("SELECT receiver_id FROM friend_request WHERE sender_id = ? AND status = 'sent'", user_id)

        if friend_id == user_id:
            response="YOU CAN'T SEND A FRIEND REQUEST TO YOURSELF"

        elif friend_id in [friend["id"] for friend in friends]:
            response="USER ALREADY FRIEND"
        elif friend_id in [requests["sender_id"] for requests in requests_received]:
            response = f"YOU HAVE RECEIVED REQUEST FROM {friend}"
        elif friend_id in [requests["receiver_id"] for requests in requests_sent]:
            response="REQUEST ALREADY SENT"
        else:
            db.execute("INSERT INTO friend_request (sender_id, receiver_id, status) VALUES (?, ?, ?)", user_id, friend_id, "sent")
            response="FRIEND REQUEST SENT"
        return render_template("addFriend.html", user=user, dp_src=file_path, friends=friends, response=response)
    else:
        info=get_user_info(session["user_id"])
        user = info["user"]
        file_path = info["dp_src"]
        friends = info["friends"]

        return render_template("addFriend.html", user=user, dp_src=file_path, friends=friends)



@app.route("/showRequests", methods=["GET", "POST"])
@login_required
def showRequests():
    if request.method == "POST":
        status = request.form.get("status").lower()
        sender_id = request.form.get("sender_id")
        user_id = session["user_id"]

        info=get_user_info(user_id)
        user = info["user"]
        file_path = info["dp_src"]
        people = info["people"]

        try:
            sender_id = int(sender_id)
        except ValueError:
            return apology("INVALID RESPONSE")

        if  status not in ["accepted", "rejected"] or sender_id not in [person["id"] for person in people]:
            return apology("INVALID RESPONSE")


        if status == "accepted":
            db.execute("INSERT INTO friends (person_id, friend_id) VALUES (?, ?)", user_id, sender_id)
        db.execute("UPDATE friend_request SET status = ? WHERE receiver_id = ? AND sender_id = ?", status, user_id, sender_id)

        requests = show_requests()
        info = get_user_info(user_id)
        friends = info["friends"]
        user = info["user"]
        return render_template("showRequests.html", user=user, dp_src=file_path, friends=friends, requests=requests, user_id=user_id)
    else:
        user_id = session["user_id"]
        info=get_user_info(user_id)
        user = info["user"]
        file_path = info["dp_src"]
        friends = info["friends"]
        requests = show_requests()

        return render_template("showRequests.html", user=user, dp_src=file_path, friends=friends, requests=requests, user_id=user_id)







@app.route("/chats", methods=["GET", "POST"])
@login_required
def chats():
    if request.method == "POST":
        friend_id = request.form.get("friend_id")
    else:
        friend_id = request.args.get("friend_id")

    try:
        friend_id = int(friend_id)
    except ValueError:
        return apology("Invalid Response")

    user_id = session["user_id"]
    info = get_user_info(user_id)
    user = info["user"]
    file_path = info["dp_src"]
    friends = info["friends"]

    friend_info = {}

    if friend_id not in [friend["id"] for friend in friends]:
        return apology("Inavlid Response")

    for friend in friends:
        if friend["id"] == friend_id:
            friend_info["id"] = friend_id
            friend_info["username"] = friend["username"]
            friend_info["dp_src"] = friend["dp_src"]
            break

    chats = db.execute("SELECT sender_id, receiver_id, message, status, timestamp FROM conversations WHERE (sender_id = ? AND receiver_id = ?) OR (receiver_id = ? AND sender_id = ?) ORDER BY timestamp ", user_id, friend_id, user_id, friend_id)

    if not chats:
        return render_template("new_chat.html", user=user, dp_src=file_path, friends=friends, friend_info=friend_info)

    for chat in chats:
        if chat["status"] == 'reached' and chat["sender_id"] == friend_id:
            chat["new-chat-divider"] = True
            break

    new_chats = db.execute("SELECT sender_id, COUNT(message) AS count_noti FROM conversations WHERE receiver_id = ? AND (status = 'sent' OR status = 'reached') GROUP BY sender_id", user_id)

    notification_count = [chat["count_noti"] for chat in new_chats if chat["sender_id"] == friend_id]
    if notification_count:
        friend_info["notification_count"]= notification_count[0]

    db.execute("UPDATE conversations SET status = 'seen' WHERE receiver_id = ? AND sender_id = ? AND status = 'reached'", user_id, friend_id)

    print(friend_id)
    print(friends)
    if new_chats:
        for friend in friends:
            print(friend["id"])
            print(friend["id"] == friend_id)
            if friend["id"] == friend_id:
                friend["notification"] = 0
                continue
            notification = [chat["count_noti"] for chat in new_chats if chat["sender_id"] == friend["id"]]
            if notification:
                friend["notification"] = notification[0]
    print(friends)

    sorted_friends = sorted(friends, key=lambda x: x['timestamp'], reverse=True)


    for index, chat in enumerate(chats):
        chat["ist"] = convert_to_ist(chat["timestamp"])

        date = get_message(chat["timestamp"])
        if not chats[index - 1] or get_message(chats[index - 1]["timestamp"]) != date:
            chat["date"] = date
        chat["status_tick"] = f"../static/media/icons/{chat["status"]}.png"

    return render_template("chats.html", user=user, dp_src=file_path, friends=sorted_friends, friend_info=friend_info, chats=chats)


@app.route("/addChats", methods=["POST"])
@login_required
def addChats():
    user_id = session["user_id"]
    friend_id = request.form.get("friend_id")
    message = request.form.get("message")

    if message == "":
        return redirect(url_for("chats", friend_id=friend_id))

    try:
        friend_id = int(friend_id)
    except ValueError:
        return apology("Invalid Response")

    info = get_user_info(user_id)
    friends = info["friends"]

    if friend_id not in [friend["id"] for friend in friends]:
        return apology("Invalid Response")

    db.execute("INSERT INTO conversations (sender_id, receiver_id, message, status) VALUES (?, ?, ?, ?)", user_id, friend_id, message, "sent")
    return redirect(url_for("chats", friend_id=friend_id))
