# PostgreSQL Migration Guide

This guide will help you migrate your Django project from SQLite to PostgreSQL and run the project locally.

## Changes Made

1. **Added PostgreSQL driver** to `requirements.txt`
2. **Updated `docker-compose.yml`** with PostgreSQL service
3. **Updated `env.sample`** with PostgreSQL configuration examples

## Prerequisites

### For Docker Setup
You need to install Docker Desktop:
- **Windows:** Download from [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **macOS:** Download from [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Linux:** Follow instructions at [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)

### For Python Setup
You need Python 3.8+ and pip installed:
- **Windows:** Download from [python.org](https://www.python.org/downloads/windows/)
- **macOS:** `brew install python` or download from [python.org](https://www.python.org/downloads/mac-osx/)
- **Linux:** `sudo apt-get install python3 python3-pip` (Ubuntu/Debian) or equivalent for your distribution

## Running the Project

### Option 1: Using Docker (Recommended)

This method runs everything in containers, including PostgreSQL and the Django application.

1. **Ensure Docker Desktop is running**

2. **Clone/navigate to the project directory:**
   ```bash
   cd /path/to/companyWebsite
   ```

3. **Create and configure your `.env` file:**
   
   **Windows (PowerShell):**
   ```powershell
   Copy-Item env.sample .env
   ```
   
   **macOS/Linux:**
   ```bash
   cp env.sample .env
   ```
   
   Then edit `.env` and uncomment/update the PostgreSQL settings:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   
   # Database Configuration
   DB_ENGINE=postgresql
   DB_HOST=db
   DB_NAME=companywebsite_db
   DB_USERNAME=companywebsite_user
   DB_PASS=companywebsite_pass
   DB_PORT=5432
   ```

4. **Export data from SQLite (if you want to preserve existing data):**
   ```bash
   # Install dependencies locally first (for Django commands)
   pip install -r requirements.txt
   python manage.py dumpdata > data_backup.json
   ```

5. **Build and start all services with Docker:**
   ```bash
   docker-compose up --build
   ```

6. **In a new terminal, run migrations inside the container:**
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

7. **Create a superuser (optional):**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

8. **Import existing data (if you exported data):**
   ```bash
   docker-compose exec web python manage.py loaddata data_backup.json
   ```

9. **Access the application:**
   - Main site: http://localhost
   - Admin panel: http://localhost/admin

10. **To stop the application:**
    ```bash
    docker-compose down
    ```

### Option 2: Using Plain Python with Local PostgreSQL

This method runs Django with `python manage.py runserver` and uses a local PostgreSQL installation.

#### Step 1: Install PostgreSQL

**Windows:**
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Add PostgreSQL to your PATH (usually done automatically)

**macOS:**
```bash
# Using Homebrew (recommended)
brew install postgresql
brew services start postgresql

# Or download from postgresql.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Linux (CentOS/RHEL/Fedora):**
```bash
sudo dnf install postgresql postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 2: Create Database and User

**Windows:**
```cmd
# Open Command Prompt as Administrator
psql -U postgres
```

**macOS:**
```bash
# If you used Homebrew
psql postgres

# If you used the installer
sudo -u postgres psql
```

**Linux:**
```bash
sudo -u postgres psql
```

Then in the PostgreSQL shell:
```sql
CREATE DATABASE companywebsite_db;
CREATE USER companywebsite_user WITH PASSWORD 'companywebsite_pass';
GRANT ALL PRIVILEGES ON DATABASE companywebsite_db TO companywebsite_user;
ALTER USER companywebsite_user CREATEDB;  -- Allow user to create test databases
\q
```

#### Step 3: Set Up Python Environment

**All Operating Systems:**

1. **Navigate to project directory:**
   ```bash
   cd /path/to/companyWebsite
   ```

2. **Create virtual environment:**
   
   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

#### Step 4: Configure Environment

1. **Create and configure your `.env` file:**
   
   **Windows (PowerShell):**
   ```powershell
   Copy-Item env.sample .env
   ```
   
   **macOS/Linux:**
   ```bash
   cp env.sample .env
   ```
   
   Then edit `.env` and uncomment/update the PostgreSQL settings:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   
   # Database Configuration
   DB_ENGINE=postgresql
   DB_HOST=localhost
   DB_NAME=companywebsite_db
   DB_USERNAME=companywebsite_user
   DB_PASS=companywebsite_pass
   DB_PORT=5432
   ```

#### Step 5: Migrate and Run

1. **Export existing SQLite data (optional):**
   ```bash
   python manage.py dumpdata > data_backup.json
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Import existing data (if you exported data):**
   ```bash
   python manage.py loaddata data_backup.json
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Main site: http://127.0.0.1:8000
   - Admin panel: http://127.0.0.1:8000/admin

#### Step 6: Daily Development

**Starting development session:**
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start the server
python manage.py runserver
```

**Stopping development:**
- Press `Ctrl+C` to stop the server
- Type `deactivate` to exit virtual environment

## Quick Reference

### Environment Variables

The following environment variables configure the database:

- `DB_ENGINE=postgresql` - Database engine
- `DB_HOST=localhost` - Database host (use `db` for Docker, `localhost` for local setup)
- `DB_NAME=companywebsite_db` - Database name
- `DB_USERNAME=companywebsite_user` - Database username
- `DB_PASS=companywebsite_pass` - Database password
- `DB_PORT=5432` - Database port

### Testing the Setup

**For Docker:**
```bash
docker-compose exec web python manage.py dbshell
docker-compose exec web python manage.py check
docker-compose exec web python manage.py test
```

**For Local Python:**
```bash
python manage.py dbshell
python manage.py check
python manage.py test
```

### Rollback to SQLite

If you need to rollback to SQLite:

1. **Comment out or remove database environment variables from `.env`**
2. **Restart the application**

The Django settings will automatically fallback to SQLite when no database environment variables are provided.

### Common Commands

**Docker Development:**
```bash
# Start services
docker-compose up

# Run Django commands
docker-compose exec web python manage.py <command>

# View logs
docker-compose logs web

# Stop services
docker-compose down
```

**Local Python Development:**
```bash
# Activate environment (daily)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## Important Notes

- **Backup your SQLite database** before migration: `cp db.sqlite3 db.sqlite3.backup`
- **PostgreSQL is case-sensitive** for table and column names
- **Different SQL syntax** - some raw SQL queries might need adjustment
- **Performance improvements** - PostgreSQL generally performs better than SQLite for web applications
- **Concurrent access** - PostgreSQL handles multiple simultaneous connections much better than SQLite

## Troubleshooting

### Connection Refused Error
- Ensure PostgreSQL service is running
- Check that the port 5432 is not blocked by firewall
- Verify connection parameters in `.env` file

### Migration Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that the database user has proper permissions
- Verify database name and credentials

### Data Import Issues
- Check for encoding issues in your SQLite data
- Some field types might need manual adjustment
- Consider using `--natural-foreign` and `--natural-primary` flags with dumpdata

For additional help, refer to the [Django database documentation](https://docs.djangoproject.com/en/4.2/ref/databases/). 