from flask import Flask, render_template, request
# from flask.globals import request
from flask_mysqldb import MySQL
from datetime import datetime
app = Flask(__name__)
app.config['DEBUG'] = True

# DB Connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PW#ams123'
app.config['MYSQL_DB'] = 'food_log'

mysql = MySQL(app)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt,'%Y%m%d')
        return database_date

    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/food', methods = ['GET', 'POST'])
def food():
    db = mysql.connection.cursor()
    if request.method == 'POST': 
        name = format(request.form['food-name'])
        protein = int(format(request.form['protein']))
        carbohydrates = int(format(request.form['carbohydrates']))
        fat = int(format(request.form['fat']))
        calories = protein*4 + carbohydrates*4 + fat*9

        #Call DB
        
        db.execute("INSERT INTO food(name, protein, carbohydrates, fat, calories) VALUES (%s, %s, %s, %s, %s)", (name, protein, carbohydrates, fat, calories))
        db.execute("SELECT name, protein, carbohydrates, fat, calories FROM food order by id desc limit 5")
        result = db.fetchall()
        results = list(result)
        mysql.connection.commit()
        db.close()
        return render_template('add_food.html', results=results)
    db.execute("SELECT name, protein, carbohydrates, fat, calories FROM food order by id desc limit 5")
    result = db.fetchall()
    results = list(result)
    return render_template('add_food.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)