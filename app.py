from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.db import init_db, seed_db, create_user, get_user_by_email, get_user_profile, get_user_expenses, get_spending_summary, get_category_breakdown, get_user_by_id
import sqlite3
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'spendly-secret-dev-key')


# ------------------------------------------------------------------ #
# Context Processors                                                    #
# ------------------------------------------------------------------ #

@app.context_processor
def inject_user():
    user_id = session.get("user_id")
    if user_id:
        user = get_user_by_id(user_id)
        return dict(current_user=user)
    return dict(current_user=None)

# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")

        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash(password)

        try:
            create_user(name, email, password_hash)
            flash("Account created successfully! Please sign in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered.")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("All fields are required.")
            return render_template("login.html")

        user = get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Successfully logged in!")
            return redirect(url_for("landing"))

        flash("Invalid email or password.")
        return render_template("login.html")

    return render_template("login.html")


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
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user = get_user_profile(user_id)
    summary = get_spending_summary(user_id)
    expenses = get_user_expenses(user_id)
    breakdown = get_category_breakdown(user_id)

    return render_template("profile.html",
                           user=user,
                           summary=summary,
                           expenses=expenses,
                           breakdown=breakdown)


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            category = request.form.get("category")
            date = request.form.get("date")
            description = request.form.get("description")

            if not category or not date:
                flash("Please fill in all required fields.")
                return render_template("add_expense.html")

            from database.db import add_expense as db_add_expense
            db_add_expense(session["user_id"], amount, category, date, description)

            flash("Expense added successfully!")
            return redirect(url_for("profile"))
        except (ValueError, TypeError):
            flash("Invalid amount entered. Please enter a numeric value.")
            return render_template("add_expense.html")

    return render_template("add_expense.html")


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def edit_expense(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Fetch the expense to ensure it belongs to the user
    from database.db import get_db
    with get_db() as conn:
        expense = conn.execute(
            'SELECT * FROM expenses WHERE id = ? AND user_id = ?',
            (id, user_id)
        ).fetchone()

    if not expense:
        flash("Expense not found or access denied.")
        return redirect(url_for("profile"))

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            category = request.form.get("category")
            date = request.form.get("date")
            description = request.form.get("description")

            if not category or not date:
                flash("Please fill in all required fields.")
                return render_template("edit_expense.html", expense=expense)

            from database.db import update_expense as db_update_expense
            if db_update_expense(id, user_id, amount, category, date, description):
                flash("Expense updated successfully!")
                return redirect(url_for("profile"))
            else:
                flash("Failed to update expense.")
                return render_template("edit_expense.html", expense=expense)
        except (ValueError, TypeError):
            flash("Invalid amount entered. Please enter a numeric value.")
            return render_template("edit_expense.html", expense=expense)

    return render_template("edit_expense.html", expense=expense)


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    from database.db import delete_expense as db_delete_expense
    if db_delete_expense(id, user_id):
        flash("Expense deleted successfully!")
    else:
        flash("Expense not found or access denied.")

    return redirect(url_for("profile"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
