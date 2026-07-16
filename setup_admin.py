import psycopg2
from psycopg2.extras import RealDictCursor

def setup_first_user():
    try:
        print("----DATABASE SETUP----")
        host_name=input("host(default localhost): ").strip().lower()
        database_name=input("database name: ").strip().lower()
        user_name=input('postgres user; ').strip().lower()
        db_password=input("postgres password : ").strip()

        conn=psycopg2.connect(
            host=host_name,
            database=database_name,
            user=user_name,
            password=db_password

        )
        cur=conn.cursor()
        username=input("username: ").strip().lower()
        id=int(input("national id: ").strip())
        password=input("password: ").strip()
        cur.execute("""INSERT INTO users(id,username,password,role)VALUES(%s,%s,%s,'manager')ON CONFLICT (username) DO NOTHING;""",(id,username,password))
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Manger {username} created succcessfully")
    except Exception as e:
        print(f"error occurred : {e}")
if __name__=="__main__":
    setup_first_user()            
