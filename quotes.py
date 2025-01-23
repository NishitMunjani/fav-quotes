from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# connection = psycopg2.connect(
#     dbname="quotes",
#     user="postgres",
#     password="123456", # This password will not work locally, you need different password.., previous one was also not working.
#     host="localhost",
#     port="5432"
# )

# cursor = connection.cursor()

# DATABASE_URL = os.getenv('postgresql://favquotes_9kvq_user:8RinzX9aO4MS0t30T0H2qcP9yNglwE38@dpg-cu7ipg3v2p9s73bgjt3g-a.oregon-postgres.render.com/favquotes_9kvq')
DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

create_table_query = """ 
CREATE TABLE IF NOT EXISTS favquotes (
    id SERIAL PRIMARY KEY,
    author VARCHAR(30),
    quote VARCHAR(2000)
);
"""
cursor.execute(create_table_query)
connection.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM favquotes")
    result = cursor.fetchall()
    return render_template('index.html', result=result)

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/process', methods=['POST'])
def process():
    author = request.form['author']
    quote = request.form['quote']
    insert_query = "INSERT INTO favquotes (author, quote) VALUES (%s, %s)"
    cursor.execute(insert_query, (author, quote))
    connection.commit()
    return redirect(url_for('index'))
