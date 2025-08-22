from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from datetime import date, timedelta, datetime
import db_helper
from typing import List, Optional
from pydantic import BaseModel
import mysql.connector
from jose import jwt, JWTError

SECRET_KEY = "super_secret_key"  # put in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class UserCreate(BaseModel):
    username: str
    password: str


class Expense(BaseModel):
    amount: float
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains "sub" (username) and "id" (user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the Expense API!"}


@app.post("/create_user/")
def create_user(user: UserCreate):
    try:
        db_helper.create_user(user.username, user.password)
        return {"message": "User created successfully"}
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@app.post("/login/")
def login(user: UserCreate):
    db_user = db_helper.get_user_by_username(user.username)
    if not db_user or not db_helper.verify_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": db_user["username"], "id": db_user["id"]}, expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}


@app.get("/expenses/", response_model=List[Expense])
def get_expenses(expense_date: date, current_user: dict = Depends(get_current_user)):
    expenses = db_helper.fetch_user_expenses(current_user["id"], expense_date)
    return expenses


@app.post("/expenses/")
def add_expense(expense_date: date, expenses: List[Expense], current_user: dict = Depends(get_current_user)):
    # Delete existing expenses for this user and date
    db_helper.delete_user_expenses_for_date(current_user["id"], expense_date)
    # Add new expenses
    for expense in expenses:
        db_helper.insert_expense(
            current_user["id"],
            expense_date,
            expense.amount,
            expense.category,
            expense.notes
        )
    return {"message": "Expenses added successfully"}
@app.get("/all_expenses/")
def get_all_expenses(current_user: dict = Depends(get_current_user)):
    expenses = db_helper.fetch_all_expenses_for_user(current_user["id"])
    return expenses

@app.post("/analytics/")
def get_analytics(date_range: DateRange, current_user: dict = Depends(get_current_user)):
    data = db_helper.fetch_user_expense_summary(
        current_user["id"],
        date_range.start_date,
        date_range.end_date
    )

    if data is None:
        raise HTTPException(status_code=500, detail="failed to fetch data")

    total = sum([row['total'] for row in data])
    breakdown = {}
    for row in data:
        percentage = row['total'] / total * 100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown


@app.get("/analytics_by_month/")
def get_analytics_by_month(current_user: dict = Depends(get_current_user)):
    data = db_helper.fetch_user_expenses_by_month(current_user["id"])
    if data is None:
        raise HTTPException(status_code=500, detail="failed to fetch data")

    return data