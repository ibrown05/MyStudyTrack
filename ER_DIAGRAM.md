# MyStudyTrack.com Entity Relationship Diagram

```mermaid
erDiagram
    SUBJECTS ||--o{ STUDY_SESSIONS : contains

    SUBJECTS {
        INTEGER id PK
        TEXT name
        TEXT color
    }

    STUDY_SESSIONS {
        INTEGER id PK
        INTEGER subject_id FK
        INTEGER minutes
        TEXT session_date
    }