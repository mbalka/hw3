from flask import Flask, render_template, request, jsonify
import sqlite3

app=Flask(__name__)

connection = sqlite3.connect('database.db')
print('opened db successfully')


connection.execute('CREATE TABLE IF NOT EXISTS foods (name TEXT, calories TEXT, cuisine TEXT, is_vegetarian TEXT, is_gluten_free TEXT)')
print('table created successfully')
connection.close()

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods=['POST'])
def addfood():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()

    try:
        name=request.form['name']
        calories=request.form['calories']
        cuisine=request.form['cuisine']
        is_vegetarian=request.form['is_vegetarian']
        is_gluten_free=request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods (name, calories, cuisine, is_vegetarian, is_gluten_free) VALUES (?,?,?,?,?)', (name, calories, cuisine, is_vegetarian, is_gluten_free))
        connection.commit()
        message='record successfully added'
    except:
        connection.rollback()
        message='error in insert operation'
    finally:
        return render_template('result.html', message=message)
        connection.close()

@app.route('/favorite')
def favorite():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    try:
        cursor.execute('SELECT * FROM foods WHERE name="sushi"')
    except:
        result='search error'
    finally:
        result=cursor.fetchone()
        connection.close()
        return jsonify(result)

@app.route('/search')
def search():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    name=(request.args.get('name'),)
    try:
        cursor.execute('SELECT * FROM foods WHERE name=?', name)
        result=jsonify(results=cursor.fetchall())
    except:
        result='search error'
    finally:
        connection.close()
        return result

@app.route('/drop')
def drop():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    try:
        cursor.execute('DROP TABLE foods')
        result='dropped'
    except:
        result='database error'
    finally:
        connection.close()
        return result
