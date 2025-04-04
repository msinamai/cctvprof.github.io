from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

DATABASE_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=TSLL-ICT-494F\\SQLEXPRESS;"
    "DATABASE=user_table;"
    "Trusted_Connection=yes;"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    address = request.form['address']
    national_id = request.form['national_id']
    date_str = request.form['date']
    message = request.form['message']

    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    try:
        conn = pyodbc.connect(DATABASE_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO [user_table].[dbo].[contact] ([name], [address], [national_id], [date], [message]) VALUES (?, ?, ?, ?, ?)",
            (name, address, national_id, date, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Contact submitted successfully.")
        return redirect(url_for('contact'))
    except Exception as e:
        flash(f"An error occurred during submission: {e}")
        return redirect(url_for('contact'))
    
@app.route('/admin_contact')
def admin_contact():
    try:
        conn = pyodbc.connect(DATABASE_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT  name, address, national_id, date, message FROM contact")
        contacts = cursor.fetchall()
        conn.close()
        return render_template('admin_contact.html', contact=contacts)
    except Exception as e:
        return f"An error occurred while fetching the contact data: {e}"

@app.route('/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    try:
        conn = pyodbc.connect(DATABASE_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM [user_table].[dbo].[contact] WHERE id = ?", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('admin_contact'))
    except Exception as e:
        return f"An error occurred while deleting the contact: {e}"


if __name__ == '__main__':
    app.run(debug=True)
