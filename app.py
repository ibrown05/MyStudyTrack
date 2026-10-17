import sqlite3
from flask import Flask, request, redirect

app = Flask(__name__)


def get_connection():
    connection = sqlite3.connect("studytrack.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            color TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            minutes INTEGER NOT NULL CHECK(minutes > 0),
            session_date TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        action = request.form["action"]
        connection = get_connection()

        if action == "add_subject":
            name = request.form["name"]
            color = request.form["color"]

            connection.execute(
                "INSERT INTO subjects (name, color) VALUES (?, ?)",
                (name, color)
            )

        elif action == "add_session":
            subject_id = request.form["subject_id"]
            minutes = request.form["minutes"]
            session_date = request.form["session_date"]

            connection.execute(
                """
                INSERT INTO study_sessions
                (subject_id, minutes, session_date)
                VALUES (?, ?, ?)
                """,
                (subject_id, minutes, session_date)
            )

        connection.commit()
        connection.close()
        return redirect("/")

    connection = get_connection()

    subjects = connection.execute(
        "SELECT * FROM subjects ORDER BY name"
    ).fetchall()

    sessions = connection.execute("""
        SELECT study_sessions.id,
       study_sessions.session_date,
               study_sessions.minutes,
               subjects.name
        FROM study_sessions
        JOIN subjects ON study_sessions.subject_id = subjects.id
        ORDER BY study_sessions.session_date DESC
    """).fetchall()
 
    total_minutes = connection.execute("SELECT COALESCE(SUM(minutes), 0) AS total FROM study_sessions").fetchone()["total"]
    connection.close()

    subject_list = ""

    for subject in subjects:
        subject_list += f"""
        <li>
            <span style="color: {subject['color']};">●</span>
            {subject['name']}
        </li>
        """

    subject_options = ""

    for subject in subjects:
        subject_options += f"""
        <option value="{subject['id']}">{subject['name']}</option>
        """

    session_list = ""

    for session in sessions:
        session_list += f"""
        <li>
            {session['session_date']} —
            {session['name']}:
            {session['minutes']} minutes

            <form method="POST"
                  action="/update_session/{session['id']}"
                  style="display:inline;">
                <input type="number"
                       name="minutes"
                       value="{session['minutes']}"
                       min="1"
                       required>
                <button type="submit">Update</button>
            </form>

            <form method="POST"
                  action="/delete_session/{session['id']}"
                  style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MyStudyTrack.com</title>
        <style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #111111;
        color: white;
        margin: 40px;
    }}

    h1 {{
        color: #e10600;
        font-size: 42px;
    }}

    h2 {{
        color: #ffffff;
        border-bottom: 2px solid #e10600;
        padding-bottom: 8px;
        max-width: 700px;
    }}

    input, select, button {{
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: none;
    }}

    button {{
        background-color: #e10600;
        color: white;
        cursor: pointer;
        font-weight: bold;
    }}

    button:hover {{
        background-color: #b80500;
    }}

    li {{
        margin: 12px;
        font-size: 18px;
    }}
</style>
    </head>
    <body>
        <h1>MyStudyTrack.com</h1>
        <p>Track your time. Improve your study.</p>

        <h2>Add a Subject</h2>

        <form method="POST">
            <input type="hidden" name="action" value="add_subject">

            <input type="text" name="name"
                   placeholder="Subject name" required>

            <select name="color">
                <option value="red">Red</option>
                <option value="blue">Blue</option>
                <option value="green">Green</option>
                <option value="purple">Purple</option>
            </select>

            <button type="submit">Add Subject</button>
        </form>

        <h2>My Subjects</h2>
        <ul>
            {subject_list}
        </ul>

        <h2>Log Study Time</h2>

        <form method="POST">
            <input type="hidden" name="action" value="add_session">

            <select name="subject_id" required>
                <option value="">Choose a subject</option>
                {subject_options}
            </select>

            <input type="number" name="minutes"
                   placeholder="Minutes" min="1" required>

            <input type="date" name="session_date" required>

            <button type="submit">Save Study Session</button>
        </form>
<h2>Total Study Time: {total_minutes} minutes</h2>
        <h2>Study Sessions</h2>
        <ul>
            {session_list}
        </ul>
    </body>
    </html>
    """
@app.route("/update_session/<int:session_id>", methods=["POST"])
def update_session(session_id):
    minutes = request.form["minutes"]

    connection = get_connection()
    connection.execute(
        "UPDATE study_sessions SET minutes = ? WHERE id = ?",
        (minutes, session_id)
    )
    connection.commit()
    connection.close()

    return redirect("/")
@app.route("/delete_session/<int:session_id>", methods=["POST"])
def delete_session(session_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM study_sessions WHERE id = ?",
        (session_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")
if __name__ == "__main__":
    init_db()
    app.run(debug=True) 