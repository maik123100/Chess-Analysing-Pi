import os
import psycopg2
from psycopg2 import sql
import questionary
from dotenv import load_dotenv, set_key
import secrets
import string

# Load .env file if it exists
load_dotenv()

def generate_password(length=16):
    """Generate a random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_env_file():
    """Create the .env file and populate it with user input for database configuration"""
    if not os.path.exists(".env"):
        # Ask if the user wants to set custom database options
        custom_settings = questionary.confirm(
            "Would you like to set custom database configuration options?").ask()

        if custom_settings:
            # Ask the user for their database settings using questionary
            db_host = questionary.text("Enter your database host (default: localhost)", default="localhost").ask()
            db_port = questionary.text("Enter your database port (default: 5432)", default="5432").ask()
            db_name = questionary.text("Enter your database name (default: chess_analyzer)", default="chess_analyzer").ask()
            db_user = questionary.text("Enter your database user (default: your_user)", default="your_user").ask()
            db_password = questionary.password("Enter your database password (leave empty for auto-generated)").ask()

            # If the user leaves the password field empty, generate one
            if not db_password:
                db_password = generate_password()

            # Write these values to the .env file
            with open(".env", "w") as env_file:
                env_file.write(f"DB_HOST={db_host}\n")
                env_file.write(f"DB_PORT={db_port}\n")
                env_file.write(f"DB_NAME={db_name}\n")
                env_file.write(f"DB_USER={db_user}\n")
                env_file.write(f"DB_PASSWORD={db_password}\n")
            
            print(f".env file created with your input values. The generated password is: {db_password}")
        else:
            # Default settings if no custom configuration is provided
            db_password = generate_password()
            with open(".env", "w") as env_file:
                env_file.write(f"DB_HOST=localhost\n")
                env_file.write(f"DB_PORT=5432\n")
                env_file.write(f"DB_NAME=chess_analyzer\n")
                env_file.write(f"DB_USER=your_user\n")
                env_file.write(f"DB_PASSWORD={db_password}\n")
            
            print(f".env file created with default values. The generated password is: {db_password}")

def connect_to_db():
    """Connect to PostgreSQL and return the connection and cursor"""
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    }
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

def create_database_if_needed():
    """Check if the database exists, if not, create it"""
    try:
        conn, cursor = connect_to_db()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (os.getenv('DB_NAME'),))
        if cursor.fetchone() is None:
            print("Database does not exist. Creating database...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv('DB_NAME'))))
            print("Database created.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables_if_needed():
    """Create necessary tables in the database if they don't exist"""
    try:
        conn, cursor = connect_to_db()
        
        # Example table creation
        create_table_query = """
        CREATE TABLE IF NOT EXISTS chess_games (
            id SERIAL PRIMARY KEY,
            game_id VARCHAR(255) NOT NULL,
            player_white VARCHAR(255),
            player_black VARCHAR(255),
            result VARCHAR(10)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tables created or already exist.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating tables: {e}")

def main():
    # Step 1: Create .env file interactively
    create_env_file()

    # Step 2: Create database and tables if needed
    create_database_if_needed()
    create_tables_if_needed()

    print("Setup completed.")

if __name__ == "__main__":
    main()
