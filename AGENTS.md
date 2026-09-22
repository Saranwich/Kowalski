# Project Context

Kowalski is intended to grow into a personal AI secretary. The first milestone is a Telegram bot that checks university coursework, detects new or changed assignments, tracks submission status, and sends deadline reminders. A Discord adapter may be added later, but both clients must share one backend and core domain.

## Course Sources

- TU Moodle: `https://moodle.tu.ac.th/`
- CS CourseWeb: `https://courses.cs.tu.ac.th/`
- Both sites expose the Moodle Official Mobile Web Service. Prefer the read-only Moodle REST API over HTML scraping.
- Use timezone `Asia/Bangkok` for all user-facing deadlines.
- API notes and verified request shapes are documented in `docs/api-interface.html`.

## Environment Variables

- `TU_moodle_username`
- `TU_moodle_password`
- `cs_courses_web_username`
- `cs_courses_web_password`

Keep `.env.example` limited to variables currently used by the project. Do not add speculative configuration.

## Security Rules

- Never print, log, commit, or include `.env` values in tool output.
- Never persist Moodle passwords, access tokens, private tokens, or session cookies.
- Use Moodle tokens only in memory and request a new token when required.
- Keep probes, raw responses, screenshots, and temporary scripts in `scratch/`; the directory is intentionally ignored by Git.
- Use read-only Moodle functions unless the user explicitly authorizes a write action.

## Integration Notes

- Authenticate with `POST /login/token.php` using service `moodle_mobile_app`.
- Call Moodle functions through `POST /webservice/rest/server.php` with JSON responses.
- Namespace remote identifiers by source, for example `tu_moodle:assign:21997`, because numeric IDs can overlap between sites.
- Assignment status may appear under either `lastattempt.submission` or `lastattempt.teamsubmission`.
- The initial product does not require LLM-generated homework summaries. Reliable fetching, change detection, deadline tracking, and notifications come first.
