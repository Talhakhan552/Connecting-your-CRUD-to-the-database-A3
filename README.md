# Task CRUD API — SQLite Version

A Flask CRUD API for managing tasks, backed by a SQLite database.

## Why SQLite

SQLite was chosen because it needs no separate database server, stores the
entire database in a single file, and comes built into Python — making it
ideal for a small project like this one.

## Where the database lives

The database file `tasks.db` is created automatically in the project folder
the first time the app runs. It is git-ignored, so every fresh clone starts
with an empty database that rebuilds itself with 3 example tasks.

## How to run

\`\`\`bash
pip install -r requirements.txt
python app.py
\`\`\`

The API will be available at `http://localhost:3000`.

## Endpoints

- `GET /tasks` — list all tasks
- `GET /tasks/<id>` — get one task
- `POST /tasks` — create a task
- `PUT /tasks/<id>` — update a task
- `DELETE /tasks/<id>` — delete a task

## Database screenshot

![Database screenshot](screenshot.png)

## Example SQL query

\`\`\`sql
DELETE FROM tasks WHERE done = 1;
\`\`\`

This deleted all tasks that had been marked done, leaving the table empty —
confirmed instantly through `GET /tasks` returning `[]`, with no server
restart needed.