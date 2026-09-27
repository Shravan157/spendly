Spec: Profile Page (Dynamic)

Overview
This feature implements the functional Profile Page for Spendly. It replaces the static, hardcoded UI with dynamic data fetched from the SQLite database. The page provides a comprehensive overview of the authenticated user's account and spending habits, serving as the central hub for user account management and financial review.

Depends on
- Step 01: Database setup
- Step 02: Registration
- Step 03: Login + Logout

Routes
- GET /profile — render the profile page — logged-in only (redirect to /login if not authenticated)

Database changes
No database changes. The existing `users` and `expenses` tables are used.

Templates
- Create: templates/profile.html — full profile page extending base.html.
    - User info card: Display name, email, and member-since date fetched from the `users` table.
    - Summary stats row: 
        - Total Spent: SUM of all expenses for the user.
        - Transaction Count: COUNT of all expenses for the user.
        - Top Category: Category with the highest total spend.
    - Transaction history table: All expenses for the user, ordered by date (DESC). Handle the "No expenses found" state with a friendly message.
    - Category breakdown: Aggregated totals and percentages per category for the user.

Files to change
- app.py — implement logic to fetch user and expense data from the DB.
- database/db.py — add helper functions to fetch user profiles, calculate summary stats, and get transaction history.
- static/css/style.css — ensure styles support dynamic content (e.g., varying table lengths).
- templates/base.html — modify the user account trigger (bottom-left avatar) to redirect to `/profile` instead of opening the account modal.

Files to create
- templates/profile.html

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via get_db()
- Parameterised queries only — never string-format SQL
- Use CSS variables — never hardcode hex values
- All templates extend base.html
- No inline styles
- Authentication guard: check session.get("user_id"); if absent, redirect(url_for("login"))
- Handle empty states gracefully: if a user has no expenses, display "No expenses recorded yet" in the history and breakdown sections.
- Category badges must use a CSS class.

Definition of done
- [ ] Visiting `/profile` without being logged in redirects to `/login`
- [ ] Visiting `/profile` while logged in displays the actual name and email of the logged-in user from the DB
- [ ] Total Spent, Transaction Count, and Top Category are calculated accurately from the `expenses` table
- [ ] Transaction history shows the real expenses for the user, ordered by newest first
- [ ] Category breakdown accurately reflects the user's spending distribution
- [ ] The bottom-left avatar trigger now redirects to `/profile` instead of triggering the modal
- [ ] Users with zero expenses see an appropriate "No expenses" message
- [ ] Navbar and Profile page contain functional logout links
- [ ] No hex colour values appear in templates — only CSS variables
