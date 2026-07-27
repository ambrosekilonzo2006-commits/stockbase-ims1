import psycopg2, bcrypt


conn = psycopg2.connect(
    host="localhost",
    database="sales_records",
    user="postgres",
    password="Ambrose@2006"
)
cur = conn.cursor()
cur.execute("SELECT username, password FROM users;")
for username, pw in cur.fetchall():
    pw_str = str(pw)
    if not pw_str.startswith("$2"):   
        hashed = bcrypt.hashpw(pw_str.encode(), bcrypt.gensalt()).decode()
        cur.execute("UPDATE users SET password=%s WHERE username=%s;", (hashed, username))
        print(f"Hashed password for: {username}")
    else:
        print(f"Already hashed: {username}")

conn.commit()
cur.close()
conn.close()
print("DONE — all passwords are now bcrypt hashed")