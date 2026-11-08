import os
from datetime import date, datetime

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import (
    CATEGORIES,
    create_expense,
    create_user,
    get_category_breakdown,
    get_db,
    get_expense_summary,
    get_expenses_by_user,
    get_top_category,
    get_user_by_email,
    get_user_by_id,
    init_db,
    seed_db,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

with app.app_context():
    init_db()
    seed_db()


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    return {"current_user": get_user_by_id(user_id) if user_id else None}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or "@" not in email:
        return render_template(
            "register.html", error="Please enter a valid name and email."
        ), 400

    if len(password) < 8:
        return render_template(
            "register.html", error="Password must be at least 8 characters."
        ), 400

    if password != confirm_password:
        return render_template(
            "register.html", error="Passwords do not match."
        ), 400

    if get_user_by_email(email) is not None:
        return render_template(
            "register.html",
            error="An account with this email already exists.",
        ), 400

    create_user(name, email, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template(
            "login.html", error="Invalid email or password."
        ), 401

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    summary = get_expense_summary(user_id)
    top_category = get_top_category(user_id)
    breakdown_rows = get_category_breakdown(user_id)
    member_since = datetime.strptime(
        user["created_at"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%d %b %Y")

    recent_expenses = [
        {
            "date": datetime.strptime(e["date"], "%Y-%m-%d").strftime("%d %b %Y"),
            "description": e["description"] or "—",
            "category": e["category"],
            "amount_display": "₹{:,.2f}".format(e["amount"]),
        }
        for e in get_expenses_by_user(user_id)[:5]
    ]

    max_category_total = breakdown_rows[0]["total"] if breakdown_rows else 0
    category_breakdown = [
        {
            "category": row["category"],
            "total_display": "₹{:,.2f}".format(row["total"]),
            "pct": (row["total"] / max_category_total * 100) if max_category_total else 0,
        }
        for row in breakdown_rows
    ]

    return render_template(
        "profile.html",
        user=user,
        expense_count=summary["count"],
        expense_total_display="₹{:,.2f}".format(summary["total"]),
        member_since=member_since,
        expenses=recent_expenses,
        top_category=top_category,
        category_breakdown=category_breakdown,
        categories=CATEGORIES,
        today=date.today().isoformat(),
    )


@app.route("/expenses/add", methods=["POST"])
def add_expense():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    amount = request.form.get("amount", "")
    category = request.form.get("category", "")
    expense_date = request.form.get("date", "")
    description = request.form.get("description", "").strip()

    try:
        amount = float(amount)
    except ValueError:
        amount = None

    if amount is None or amount <= 0 or category not in CATEGORIES or not expense_date:
        return redirect(url_for("profile"))

    create_expense(user_id, amount, category, expense_date, description)
    return redirect(url_for("profile"))


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
