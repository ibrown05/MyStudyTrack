# MyStudyTrack.com Database Design

## Tables

### Subjects

Stores each school subject.

| Column | Description |
|---|---|
| `id` | Primary key |
| `name` | Subject name |
| `color` | Display color |

### Study Sessions

Stores each study session.

| Column | Description |
|---|---|
| `id` | Primary key |
| `subject_id` | Foreign key connected to `subjects.id` |
| `minutes` | Number of minutes studied |
| `session_date` | Date of the study session |

## Relationship

One subject can have many study sessions.

The relationship is:

`subjects.id` → `study_sessions.subject_id`

This prevents repeating the subject name every time a study session is saved.

## Database Operations

The application uses:

- `INSERT` to add subjects and study sessions
- `SELECT` to display subjects and sessions
- `UPDATE` to edit study-session minutes
- `DELETE` to remove study sessions
- `JOIN` to display the subject name with each session
- `SUM` to calculate total study time

## Integrity Rules

- Every subject must have a name and color.
- Every study session must belong to a subject.
- Study minutes must be greater than zero.
- Primary keys uniquely identify each record.
- The foreign key connects study sessions to subjects.