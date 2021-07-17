from flask import Flask, render_template, request
# from flask.globals import request
import MySQLdb

app = Flask(__name__)
app.config['DEBUG'] = True

# DB Connection 
db = MySQLdb.connect("localhost","root","PW#ams123","food_log" )

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/food', methods = ['GET', 'POST'])
def food():
    cur = db.cursor()
    if request.method == 'POST': 
        name = format(request.form['food-name'])
        protein = int(format(request.form['protein']))
        carbohydrates = int(format(request.form['carbohydrates']))
        fat = int(format(request.form['fat']))
        calories = protein*4 + carbohydrates*4 + fat*9

        #Call DB
        
        cur.execute("INSERT INTO food(name, protein, carbohydrates, fat, calories) VALUES (%s, %s, %s, %s, %s)", (name, protein, carbohydrates, fat, calories))
        db.commit()
        cur.close()
        return '<h1>Name: {}</h1>'.format(request.form['food-name'])
    cur.execute("SELECT name, protein, carbohydrates, fat, calories FROM food")
    results = cur.fetchall()
    # rows = []
    # for row in results: 
    #     rows.append(row) 

    # # result = list(results)
    # results = rows
    return render_template('add_food.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)