from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

connection = psycopg2.connect(
    dbname="quotes",
    user="postgres",
    password="mnk#1234",
    host="localhost",
    port="5432"
)

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
