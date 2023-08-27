from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database initialization and setup
db_path = 'church_members.db'

if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE Members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            email TEXT,
            address TEXT,
            date_of_birth DATE,
            date_joined DATE,
            gender TEXT,
            marital_status TEXT,
            occupation TEXT,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_member', methods=['POST'])
def add_member():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    # Extract other form fields similarly...

    c.execute('''
        INSERT INTO Members (first_name, last_name, contact_number, email, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, contact_number, email, address))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if request.method == 'POST':
        # Update the member information
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']

        c.execute('''
            UPDATE Members SET
            first_name = ?,
            last_name = ?,
            contact_number = ?,
            email = ?,
            address = ?
            WHERE member_id = ?
        ''', (first_name, last_name, contact_number, email, address, member_id))

        conn.commit()
        conn.close()

        return redirect(url_for('view_members'))

    else:
        c.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,))
        member = c.fetchone()

        conn.close()

        return render_template('edit_member.html', member=member)


@app.route('/delete_member/<int:member_id>', methods=['GET', 'POST'])
def delete_member(member_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if request.method == 'POST':
        c.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('view_members'))

    else:
        c.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,))
        member = c.fetchone()

        conn.close()

        return render_template('delete_member.html', member=member)


@app.route('/view_members')
def view_members():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT * FROM Members')
    members = c.fetchall()

    conn.close()

    return render_template('view_members.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)
