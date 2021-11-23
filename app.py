from flask import Flask
from flask import render_template
from flask import request
import time
import pyodbc 
import process as p


app = Flask(__name__)


# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=StackOverflow;Trusted_Connection=yes;')
# cursor = conn.cursor()

# start_time = time.time()
# cursor.execute('SELECT * FROM dbo.Badges')
# print("--- %s seconds ---" % (time.time() - start_time))


@app.route('/')
def index():
      return render_template('index.html')


@app.route('/brain')
def brain():
    return render_template("brain.html")

@app.route('/result', methods = ['POST'])
def result():
    # print(request.data)
    # print(request.form)
    # print(type(request.form))

    user_input = request.form.to_dict()['user-input']
    # print(user_input)
    print(type(user_input))
    print('user_input is {}'.format(user_input))

    rs, rw = p.getTopics(user_input)
    # print(user_input_tokenized)
    return render_template("result.html", input = user_input, value1 = rs, value2 = rw)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

