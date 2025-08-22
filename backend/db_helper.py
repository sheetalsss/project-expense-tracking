import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
from passlib.context import CryptContext
from datetime import date
logger = setup_logger('db_helper')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@contextmanager
def get_db_cursor(commit=False):
    mysql_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dand@2018',
        database='expense_manager'
    )

    if mysql_connection.is_connected():
        print('MySQL connection is connected')
    else:
        print('MySQL connection is not connected')

    cursor = mysql_connection.cursor(dictionary=True)
    yield cursor

    if commit:
        mysql_connection.commit()
    cursor.close()
    mysql_connection.close()
#############################################################################

def create_user(username: str, password: str):
    logger.info(f'Creating user: {username}')
    hashed_password = pwd_context.hash(password)
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            (username, hashed_password)
        )

def verify_user(username: str, password: str) -> bool:
    logger.info(f'Verifying user: {username}')
    with get_db_cursor() as cursor:
        cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        return result and pwd_context.verify(password, result['hashed_password'])


def get_user_by_username(username: str):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()


def fetch_user_expenses(user_id: int, expense_date: date):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT expense_date, amount, category, notes FROM expenses WHERE expense_date = %s AND user_id = %s",
            (expense_date, user_id)
        )
        return cursor.fetchall()



###############################################################
def fetch_expense_for_date(expense_date):
    logger.info('Fetching expense for date: {}'.format(expense_date))
    with get_db_cursor() as cursor:
        cursor.execute('select * from expenses where expense_date=%s', (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def fetch_all_user_expenses(user_id: int):
    logger.info(f'Fetching all user expenses {user_id}')
    with get_db_cursor() as cursor:
        cursor.execute('select expense_date, amount, category, notes from expenses where user_id = %s', (user_id,))
        return cursor.fetchall()

def fetch_user_expenses_by_month(user_id: int):
    logger.info(f'Fetching monthly expenses for user {user_id}')
    with get_db_cursor() as cursor:
        cursor.execute('''select DATE_FORMAT(expense_date, '%Y-%m') AS month_year, 
                                 SUM(amount) AS total_amount from expenses 
                          WHERE user_id = %s
                          GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
                          ORDER BY month_year;''', (user_id,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(user_id: int, expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (user_id, expense_date, amount, category, notes) VALUES (%s, %s, %s, %s, %s)",
            (user_id, expense_date, amount, category, notes)
        )


def fetch_user_expense_summary(user_id: int, start_date: date, end_date: date):
    logger.info(f'Fetching expense summary for user {user_id} from {start_date} to {end_date}')
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date BETWEEN %s AND %s AND user_id = %s
               GROUP BY category;''',
            (start_date, end_date, user_id)
        )
        expenses = cursor.fetchall()
        return expenses

def delete_user_expenses_for_date(user_id: int, expense_date: date):
    logger.info(f'Deleting expenses for user {user_id} on date: {expense_date}')
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            'DELETE FROM expenses WHERE expense_date=%s AND user_id=%s',
            (expense_date, user_id)
        )

if __name__ == '__main__':
    # delete_expenses_for_date('2024-08-20')
    # fetch_expense_for_date('2024-08-20')
    summary = fetch_expense_summary('2024-08-01','2024-08-05')
    for record in summary:
        print(record)