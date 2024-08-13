# Chess-Analysing-Pi

This project analyzes chess games and stores the results in a database.

## Setup

To run this project, you need to set up a PostgreSQL database and create an environment file with your database and chess.com credentials.

### Database Setup

1. Install PostgreSQL on your machine.
2. Create a new PostgreSQL database for this project.
3. In the new database, create a table named `games` with the following columns:
    - `uuid` (VARCHAR(255) PRIMARY KEY)
    - `white_username` (VARCHAR(255))
    - `white_rating` (INTEGER)
    - `black_username` (VARCHAR(255))
    - `black_rating` (INTEGER)
    - `time_control` (VARCHAR(50))
    - `pgn` (TEXT)
    - `win` (VARCHAR(10))

### Environment File Setup

1. In the root of the project, create a new file named `.env`.
2. In the `.env` file, add the following lines:

```properties
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
CHESS_USERNAME=your_chess.com_username
# ENV_Test can be one of the following:
# - dev: for development environment
# - test: for testing environment
# - prod: for production environment
ENV_Test=prod
```

### Installing Dependencies

Run the following command to install the necessary Python packages:

```sh
pip install -r requirements.txt
```

### Running the Project

To initialize the database with the last month's worth of games, run:

```sh
python3 ChessDB_updating_service.py init
```

To run the standard execution, which fetches today's games, run:

```sh
python3 ChessDB_updating_service.py std
```

### Automating the Process

You can automate the standard execution to run daily at 11 PM by using the provided shell script. Run the following command:

```sh
./start_ChessDB_updating_service.sh
```

This script will:
1. Check if the necessary Python packages are installed.
2. Run the initialization command.
3. Create a cron job to run the standard execution at 11 PM daily.