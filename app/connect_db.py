import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # get secret data from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(dbname="FRPokedex", host="localhost", user=DB_USER, password=DB_PASSWORD, port="5432")
print(("this shiii failed :(", 'ok!')[bool(conn)])

cursor = conn.cursor()

def check_user_exist(login, email = 'null', phone = 'null'):
    cursor.execute(f"""SELECT user_name, user_email, user_phone, user_password 
                       FROM user_data 
                       WHERE user_name='{login}' OR user_email='{email}' OR user_phone='{phone}'""")
    user = cursor.fetchone()
    if user:
        return {"username": user[0], "email": user[1], "phone": user[2], "password": user[3]}
    return None

def create_user(login, email, phone, password):
    user_exist = check_user_exist(login, email, phone)
    if not user_exist:
        cursor.execute(f"INSERT INTO user_data (user_name, user_email, user_phone, user_password) VALUES ('{login}', '{email}', '{phone}', '{password}')")
        conn.commit()
        print('User data hass been added successfuly!')
        return None
    return user_exist