# 🚀 FastSeeder

FastSeeder is a lightweight, plug-and-play seed manager for Python projects using **SQLAlchemy** as ORM.  
It allows you to **create**, **organize**, and **run database seeds** in a clean and consistent way — across any environment.

---

## ✨ What does it do?

- ✅ Automatically creates seeds in a structured format
- ✅ Executes seeds that haven't been run yet
- ✅ Tracks seed history to avoid duplicates
- ✅ Uses `SQLAlchemy` to run raw SQL or ORM logic
- ✅ Works out-of-the-box with `.env` or via secret managers like GCP Secret Manager

---

## 🧠 Who is this for?

This tool is built for **developers using SQLAlchemy** who want a simple, extensible way to manage database seed logic in any Python application.

---

## 🏗️ Folder structure

By default, FastSeeder creates your seeds in:

```
database/
└── seeds/
    └── YYYY-MM-DD-HH:MM:SS-seed-name.py
```

You can change this location by setting the environment variable:

```env
SEED_LOCATION=your/custom/path
```

---

## ⚙️ Environment variables

| Variable                         | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `DATABASE_URL`                   | URI to connect to your database (if not using secret manager)              |
| `SEED_LOCATION`                  | Path where seeds will be created/read (default: `database/seeds`)          |
| `LOG_QUERIES`                    | Set to `true` to enable SQLAlchemy logging                                 |
| `FASTSEEDER_CONNECTOR`           | Optional. One of: `gcs`, `aws` (GCS implemented, AWS in progress)          |
| `GCP_PROJECT_ID`                 | (Only for GCS connector) Your Google Cloud project ID                      |
| `GCS_DB_URI_SECRET_NAME`         | (Only for GCS connector) Name of the secret that stores your DB URI        |
| `GCS_DB_URI_SECRET_VERSION`      | Optional. Defaults to `"latest"`                                           |

---

## 🔌 Connectors

FastSeeder supports pluggable secret managers to load the database URI.

| Connector | Install Command            | Status        |
|-----------|----------------------------|---------------|
| GCS       | `pip install fastseeder[gcs]` | ✅ Implemented |
| AWS       | `pip install fastseeder[aws]` | 🚧 In progress |

---

## 📦 Installation

### Basic (with `.env`)

```bash
pip install fastseeder
```

### With Google Cloud Secret Manager

```bash
pip install fastseeder[gcs]
```

Set in your `.env`:

```env
FASTSEEDER_CONNECTOR=gcs
GCP_PROJECT_ID=your-project-id
GCS_DB_URI_SECRET_NAME=your-secret-name
```

---

## 🚀 Usage

### Create a seed

```bash
run-seeds make "seed name"
```

This will create a timestamped seed file under `database/seeds/`.

### Run all pending seeds

```bash
run-seeds seed 
```

All pending seeds will be displayed in a list for the user to confirm before execution.

### Run all pending seeds without asking confirmation

```bash
run-seeds seed --yes
```

Seeds are only executed once and tracked using a `seed_history` table in your DB.

---

## 📌 Notes

- Seeds must extend `BaseSeed` and define a unique `seed_id`.
- You can define `run()` and optionally `rollback()` logic inside the class.
- The CLI tool auto-detects pending seeds and runs them in chronological order.
- Ideal for microservices and shared DB workflows.

---

## 📚 License

MIT — use it freely and contribute if you like!