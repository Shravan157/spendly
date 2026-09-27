Spec: UI Refinement

Overview
This feature focuses on polishing the overall visual identity and user experience of Spendly. While the core functionality of the profile and auth pages is implemented, the current UI needs refinement to look professional, modern, and consistent. This includes updating the global color palette, improving typography, adding subtle animations, and ensuring a consistent layout across all pages.

Depends on
No previous steps required, but applies to all currently implemented pages (Landing, Register, Login, Profile).

Routes
No new routes.

Database changes
No database changes.

Templates
Modify:
- `templates/base.html`: Update global layout, navigation bar, and footer.
- `templates/landing.html`: Refine the hero section, call-to-action buttons, and feature grid.
- `templates/register.html`: Improve form layout, input styling, and accessibility.
- `templates/login.html`: Improve form layout, input styling, and accessibility.
- `templates/profile.html`: Refine the KPI cards, transaction table, and category breakdown visuals.

Files to change
- `static/css/style.css`: Major updates to global variables, typography, and component styles.
- `static/css/landing.css`: Refine landing-page specific layouts.
- `templates/base.html`
- `templates/landing.html`
- `templates/register.html`
- `templates/login.html`
- `templates/profile.html`

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
- Implement a cohesive color palette using CSS variables in `style.css`
- Ensure all interactive elements have clear `:hover` and `:focus` states
- Use a modern, sans-serif font stack

Definition of done
- [ ] Landing page looks modern and professional across different screen widths.
- [ ] Login and Register forms are centered, clean, and have clear validation feedback.
- [ ] Profile page KPI cards have a distinct, polished look.
- [ ] The transaction table in the profile page is legible and well-spaced.
- [ ] Category progress bars have smooth transitions and consistent colors.
- [ ] Navigation bar is consistent across all pages and provides clear feedback on active state.
