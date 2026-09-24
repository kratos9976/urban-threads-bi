# Step 3 — PostgreSQL Setup (Windows)

## 1. Install PostgreSQL
1. Go to https://www.postgresql.org/download/windows/ and download the installer (EDB installer).
2. Run it. When prompted:
   - Set a password for the `postgres` superuser — **remember this**, you'll need it below.
   - Keep the default port `5432`.
   - It installs **pgAdmin 4** alongside — a GUI you can use instead of the command line if you prefer.
3. Finish the installer.

## 2. Create the database
Open **pgAdmin 4** (search for it in the Start menu), connect using the password you set,
right-click "Databases" → "Create" → "Database", name it `urban_threads`, and save.

Or, from PowerShell (psql needs to be on PATH — the installer usually adds it):
```powershell
psql -U postgres
# enter your password when prompted
CREATE DATABASE urban_threads;
\q
```

## 3. Create a `.env` file in your project root
In VS Code, create a new file named `.env` (same level as `data/`, `sql/`, `src/`) with:
```
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=urban_threads
```
This file is already in `.gitignore`, so it won't be committed — good, since it has your password.

## 4. Install the Python packages needed to talk to Postgres
With your venv active:
```powershell
pip install psycopg2-binary sqlalchemy python-dotenv
```

## 5. Run the schema
```powershell
psql -U postgres -d urban_threads -f sql/schema.sql
```
This creates all 8 tables (stores, products, customers, orders, order_items, inventory, returns, discounts).

## 6. Load the data
```powershell
python src/load_to_postgres.py
```
You should see a line printed for each table confirming how many rows loaded.

## 7. Verify
In pgAdmin (or `psql -U postgres -d urban_threads`), run:
```sql
SELECT COUNT(*) FROM orders;
```
You should get 7,851 — matching the dataset generator's output.

## 8. Try the KPI queries
Open `sql/kpi_queries.sql` in pgAdmin's Query Tool (or psql) and run each query one at a time
to see revenue by region, AOV, return rates, and the built-in Melbourne dip.
