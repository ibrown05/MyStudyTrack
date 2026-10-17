# MyStudyTrack.com

MyStudyTrack.com is a study-time tracking web application. Users can create subjects, record study sessions, view total study time, update session minutes, and delete sessions.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS

## Database Design

The application uses two related tables:

### Subjects

- `id` — Primary key
- `name` — Subject name
- `color` — Display color

### Study Sessions

- `id` — Primary key
- `subject_id` — Foreign key connected to the Subjects table
- `minutes` — Number of minutes studied
- `session_date` — Date of the study session

## How to Run the Application

1. Open the project folder in VS Code.
2. Open the terminal.
3. Activate the virtual environment:

```bash
source .venv/bin/activate
