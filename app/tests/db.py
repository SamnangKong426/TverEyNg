import streamlit as st
import sqlite3

# Create DB and table on app startup
def create_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insert a new user into the database
def insert_user(name, age):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()

# Fetch all users from the database
def fetch_users():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

# Streamlit interface
def main():
    st.title("SQLite with Streamlit")

    # Create the database on app start
    create_db()

    # User input form
    with st.form(key="user_form"):
        name = st.text_input("Enter Name")
        age = st.number_input("Enter Age", min_value=0, max_value=100)
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if name and age:
                insert_user(name, age)
                st.success("User added successfully!")

    # Display users
    st.subheader("Users List")
    users = fetch_users()

    if users:
        for user in users:
            st.write(f"ID: {user[0]} | Name: {user[1]} | Age: {user[2]}")
    else:
        st.write("No users found!")

if __name__ == "__main__":
    main()
