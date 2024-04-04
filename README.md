# Chess-Analysing-Pi

This project analyzes chess games and stores the results in a database.

## Setup

To run this project, you need to set up a MySQL database and create an environment file with your database and chess.com credentials.

### Database Setup

1. Install MySQL on your machine.
2. Create a new MySQL database for this project.
3. In the new database, create a table named `games` with the following columns:
    - `id` (INT, primary key, auto increment)
    - `white_username` (VARCHAR(255))
    - `white_rating` (INT)
    - `black_username` (VARCHAR(255))
    - `black_rating` (INT)
    - `time_control` (INT)
    - `pgn` (TEXT)

### Environment File Setup

1. In the root of the project, create a new file named `.env`.
2. In the `.env` file, add the following lines:

```properties
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
CHESS_USERNAME=your_chess.com_username
