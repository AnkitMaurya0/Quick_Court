from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, hashlib, random, smtplib, ssl
import os

app = Flask(__name__)
app.secret_key = "secret_key"
DB = "quickcourt.db"

# -------------------- HELPERS --------------------

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------- INITIALIZE DEFAULT ADMIN --------------------
def create_default_admin():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    
    # Check if admin exists
    cur.execute("SELECT * FROM users WHERE role='admin'")
    admin = cur.fetchone()
    
    if not admin:
        default_admin_email = "admin@quickcourt.com"
        default_admin_password = hash_password("Admin@123")
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?)",
            ("Admin", default_admin_email, default_admin_password, "admin", "default.png")
        )
        print("✅ Default admin created in DB.")
    
    con.commit()
    con.close()

create_default_admin()

# Send OTP via Email
def send_email(to_email, otp):
    sender = "robogyaanx@gmail.com"
    password = "tdeuxipiiuczcthm"   # Gmail App Password
    subject = "OTP Verification"
    body = f"Your OTP is: {otp}"
    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(sender, password)
        server.sendmail(sender, to_email, message)

# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("home.html")

# Signup route (avatar upload removed → default.png)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = hash_password(request.form["password"])
        role = request.form["role"]

        filename = "default.png"  # fixed avatar for all users

        otp = f"{random.randint(0, 9999):04d}"
        session["temp_user"] = {
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "avatar": filename
        }
        session["otp"] = otp

        send_email(email, otp)
        return redirect(url_for("verify"))

    return render_template("signup.html")

# OTP Verify route
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        if user_otp == session.get("otp"):
            user = session["temp_user"]

            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password_hash, role, avatar) VALUES (?, ?, ?, ?, ?)",
                (user["name"], user["email"], user["password"], user["role"], user["avatar"])
            )
            con.commit()
            con.close()

            session.pop("temp_user", None)
            session.pop("otp", None)
            return redirect(url_for("login"))
        else:
            return "❌ Wrong OTP, try again."

    return render_template("verify_otp.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hash_password(request.form["password"])

        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, password))
        user = cur.fetchone()
        con.close()

        if user:
            session["user"] = user["email"]
            session["role"] = user["role"]
            session["name"] = user["name"]
            session["avatar"] = user["avatar"]

            # Role-based redirect
            if user["role"] == "user":
                return redirect(url_for("user_dashboard"))
            elif user["role"] == "owner":
                return redirect(url_for("owner_dashboard"))
            elif user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
        else:
            return "❌ Invalid login credentials."

    return render_template("login.html")

# Forgot password
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]

        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        con.close()

        if user:
            otp = f"{random.randint(0, 9999):04d}"
            session["reset_email"] = email
            session["otp"] = otp
            send_email(email, otp)
            return redirect(url_for("reset_password"))

        return "❌ Email not registered."

    return render_template("forgot.html")

# Reset password
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        otp = request.form["otp"]
        new_password = hash_password(request.form["password"])

        if otp == session.get("otp") and "reset_email" in session:
            email = session["reset_email"]

            con = sqlite3.connect(DB)
            cur = con.cursor()
            cur.execute("UPDATE users SET password_hash=? WHERE email=?", (new_password, email))
            con.commit()
            con.close()

            session.pop("reset_email", None)
            session.pop("otp", None)

            return "✅ Password reset successful! <a href='/login'>Login</a>"

        return "❌ Wrong OTP or session expired."

    return render_template("reset_password.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------- Dashboards --------------------
@app.route("/user/dashboard")
def user_dashboard():
    if "role" in session and session["role"] == "user":
        return render_template("user_dashboard.html", name=session["name"], avatar=session["avatar"])
    return redirect(url_for("login"))

@app.route("/owner/dashboard")
def owner_dashboard():
    if "role" in session and session["role"] == "owner":
        return render_template("owner_dashboard.html", name=session["name"], avatar=session["avatar"])
    return redirect(url_for("login"))

@app.route("/admin/dashboard")
def admin_dashboard():
    if "role" in session and session["role"] == "admin":
        return render_template("admin_dashboard.html", name=session["name"], avatar=session["avatar"])
    return redirect(url_for("login"))

@app.route("/venues")
def venues():
    # Later you can fetch venue list from quickcourt.db
    # For now, we’ll just render the HTML template
    return render_template("venues.html")

# Single Venue Page Route
@app.route("/venue/<int:venue_id>")
def single_venue(venue_id):
    # Later you can query DB: SELECT * FROM venues WHERE id = venue_id
    # For now, pass dummy data to test
    venue = {
        "id": venue_id,
        "name": "Elite Sports Arena",
        "description": "A premium multi-sport complex with indoor and outdoor courts.",
        "address": "123 Sports Street, City Center",
        "sports": ["Badminton", "Tennis", "Football"],
        "amenities": ["Parking", "Cafeteria", "Locker Rooms", "Showers"]
    }
    return render_template("single_venue.html", venue=venue)

@app.route("/court-booking")
def court_booking():
    return render_template("court_booking.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")



@app.route("/my-bookings")
def my_bookings():
    return render_template("my_bookings.html")



# -------------------- MAIN --------------------
if __name__ == "__main__":
    app.run(debug=True)
