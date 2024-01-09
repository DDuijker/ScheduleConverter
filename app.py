from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from scheduler import read_schedule_csv, create_calendar_events, export_calendar
import os
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './schedules'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.secret_key = 'nissan_secret_key'
FOOTER_LINES = 9
# Constants for working hours and standby hours
WORK_START_HOUR, WORK_START_MINUTES = 19, 0
WORK_END_HOUR, WORK_END_MINUTES = 22, 0
STANDBY_START_HOUR, STANDBY_START_MINUTES = 18, 0
STANDBY_END_HOUR, STANDBY_END_MINUTES = 19, 30
EMPLOYEES = ["Djoeke", "Menno", "Devinio"]

# Amsterdam time zone
AMSTERDAM_TZ = pytz.timezone('Europe/Amsterdam')


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    """Checks if filename has a '.' and has an allowed extension. Returns boolean"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def check_and_save_csv_file(file):
    """Checks if file is existent and is secured. Stores file in upload folder. Returns file path or flashes an error
    message"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path
    else:
        flash('Invalid file format. Please upload a CSV file.', 'error')  # Added 'error' category
        return None


@app.route('/generate', methods=['POST'])
def generate():
    """Posts the data and returns the schedule as an ics file"""
    name = request.form['name'].title()

    # Check if the post request has the file part
    if 'csvFile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    csv_file = request.files['csvFile']

    # If the user does not select a file, the browser also
    # submits an empty part without filename
    if csv_file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    csv_file_path = check_and_save_csv_file(csv_file)
    if csv_file_path:
        # Process the CSV file
        schedule_df = read_schedule_csv(csv_file_path, FOOTER_LINES)
        generated_calendar = create_calendar_events(
            name,
            schedule_df,
            WORK_START_HOUR, WORK_START_MINUTES, WORK_END_HOUR, WORK_END_MINUTES,
            STANDBY_START_HOUR, STANDBY_START_MINUTES, STANDBY_END_HOUR, STANDBY_END_MINUTES
        )

        # Set Amsterdam timezone for the events
        for event in generated_calendar.events:
            event.begin = event.begin.replace(tzinfo=pytz.utc).astimezone(AMSTERDAM_TZ)
            event.end = event.end.replace(tzinfo=pytz.utc).astimezone(AMSTERDAM_TZ)

        file_path = f'./calendars/{name}_schedule.ics'
        export_calendar(generated_calendar, file_path)

        return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
