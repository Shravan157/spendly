Spec: Login and Logout

Overview
This feature implements user authentication for Spendly. It converts the `/login` stub into a functional POST handler that verifies credentials against the database, stores the authenticated user's ID in the session, and redirects to the landing page (until a dashboard exists). It also implements the `/logout` stub, which clears the session and redirects to the landing page. After this step, the app can distinguish logged-in users from guests, which is a prerequisite for all expense features.

Depends on
- Step 01 — Database Setup
- Step 02 — Registration

Routes
- `GET /login` — render login form — public
- `POST /login` — validate credentials, set session, redirect — public
- `GET /logout` — clear session, redirect to `/` — public

Database changes
No database changes.

Templates
Modify: `templates/login.html` — add a POST form with email and password fields, flash message display, and a link to registration.

Files to change
- `app.py` — implement login (GET/POST) and logout routes.
- `database/db.py` — add `get_user_by_email(email)` helper.
- `templates/login.html` — update with login form and flash alerts.

Files to create
No new files.

New dependencies
No new dependencies.

Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend base.html
- Use `session["user_id"]` for authentication state.
- Generic "Invalid email or password" flash on login failure.

Definition of done
- [ ] Visiting `/login` renders the login form.
- [ ] Successful login with `demo@spendly.com` / `demo123` redirects to `/`.
- [ ] Incorrect credentials show a generic flash error and keep user on `/login`.
- [ ] Visiting `/logout` clears the session and redirects to `/`.
- [ ] Verify that `/logout` no longer returns a stub string.
