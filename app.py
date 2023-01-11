from flask import Flask, render_template, request
import csv
from datetime import datetime, date

app = Flask(__name__)

def read_data_from_csv():
    data = []
    with open('work_hours.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append({'hours': row[0], 'start_time': row[1], 'end_time': row[2]})
    return data

@app.route('/')
def index():
    today = date.today()
    return render_template('index.html', today=today.strftime("%Y-%m-%d"))

@app.route('/submit', methods=['POST'])
def submit():
    date_str = request.form['date']
    start_time_str = request.form['start_time']
    end_time_str = request.form['end_time']
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start_time = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M")
    work_hours = round((end_time - start_time).total_seconds() / 3600, 2)
    formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M")
    formatted_end_time = end_time.strftime("%Y-%m-%d %H:%M")
    if work_hours > 10.75:
        return 'The number of hours entered is above the maximum limit'
    else:
        with open('work_hours.csv', mode='a') as csv_file:
            fieldnames = ['hours','start_time','end_time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'hours': work_hours,'start_time':start_time,'end_time':end_time})
    return render_template('success.html', hours=work_hours, start_time=formatted_start_time, end_time=formatted_end_time)

@app.route('/history')
def history():
    # Code to read data from CSV file and store it in a variable
    data = read_data_from_csv()
    return render_template('history.html', data=data)
 
 
if __name__ == '__main__':
    app.run()