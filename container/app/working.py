from flask import Flask, render_template, make_response, redirect, request,url_for,jsonify
import mysql.connector

app = Flask(__name__)

#connting to Databse employee through the connection string

def connectDB():
  return (mysql.connector.connect(user='root', password='root',
                host='db',database='employee', port='5000'))




# route to index page

@app.route('/', methods = ['GET','POST'])
def hello_world():

# getting the user information from the web

    if request.method == 'POST':
        cnx = connectDB()
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        age = request.form['age']
        sex = request.form['sex']

# saving the data to the data base
        if first_name is not None:
            cur = cnx.cursor()
            cur.execute('INSERT INTO info (first_name,last_name,age,sex) VALUES ("%s", "%s","%s", "%s")' % (first_name, last_name, age, sex))
            cnx.commit()
            cur.close()
            cnx.close()

            return render_template('index.html')


    return render_template('index.html')


def calc_avg(option):
    cnx = connectDB()
    cursor = cnx.cursor()
    query = "SELECT " +option+ " FROM `info`"
    cursor.execute(query)
    names = list(cursor.fetchall())
    print(names)
    names = [x[0] for x in names]
    print(names)
    sum = 0
    total = 1
    if names:

        for name in names:
            sum += len(name)
        total = len(names)

    return 'Average = '+ str(sum / total)


#using select query to get requested data from database
@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        cnx = connectDB()
        cur = cnx.cursor()
        search = request.form['search']
        option = request.form.get('selectOption')
        sql = "select count(*), (length("+option+")) from info where " + option + " like '%" + search + "%'"
        cur.execute(sql)
        #count_sql = cur.fetchall()
        result = cur.fetchone()
        cnx.commit()
        cur.close()
        cnx.close()
        result = 'Count = '+str(result[0]) + ' length = '+str(result[1]);
        results = str(result) + ' ' +calc_avg(option)
        return render_template('index.html',details = results )



#using the constaints of rest api , converting the result object to json fromat and returning complete list of input recieved
@app.route('/all',methods=['GET','POST'])
def all():
    records = []
    if request.method == 'GET':
        cnx = connectDB()
        cur = cnx.cursor()
        sql = "SELECT * FROM info"
        cur.execute(sql)
        #fetchting  - selecting all the values and then getting their value one by one using cursor
        rv = cur.fetchall()

        # for row in rv:
        #     tuple = (row[0], row[1], row[2], row[3])
        #     records.append(tuple)

    payload = []
    content = {}
    for result in rv:
        content = {'first_name': result[0], 'last_name': result[1], 'age': result[2],'sex':result[3]}
        payload.append(content)
        content = {}
    return jsonify(payload)

    #TO DISPLAY LIST OF USERS IN A TABLE FORMAT
    #return render_template('index.html', all = records)





if __name__ == '__main__':
    app.run()(host='0.0.0.0')
