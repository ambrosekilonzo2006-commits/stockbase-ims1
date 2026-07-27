import psycopg2
import bcrypt
class  DatabaseRepository:
    def __init__(self,db_config):
        self.conn=psycopg2.connect(**db_config)
        self.conn.autocommit=False
    def execute_query(self,query,params=None, fetch=False):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            self.conn.commit()
            return True
        
    def verify_user(self, username, password):
        query = """
        SELECT role, password
        FROM users
        WHERE username = %s;
    """

        output = self.execute_query(
            query,
            (username,),
            fetch=True
    )

        if not output:
            return None

        role, hashed_password = output[0]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
    ):
            return role

        return None
    def add_product(self,name,stock,price,buying_price):
        que="INSERT INTO products(product_name,stock,price,buying_price)VALUES(%s,%s,%s,%s);"
        return self.execute_query(que,(name,stock,price,buying_price))
    def get_product(self,name):
        que=("SELECT * FROM products WHERE product_name=%s;")
        out=self.execute_query(que,(name,), fetch=True)
        return out[0] if out else None
    def get_whole_table(self):
        return self.execute_query("SELECT* FROM products;", fetch=True)
    def record_sale(self,name,phone,product_name,quantity):
        cur=self.conn.cursor()
        cur.execute("""INSERT INTO customers(customer_name,phone)VALUES(%s,%s)ON CONFLICT (phone)DO UPDATE  SET customer_name=EXCLUDED.customer_name RETURNING customer_id;""",(name,phone))
        
        cust_id=cur.fetchone()[0]
        cur.execute("SELECT product_id FROM products WHERE product_name=%s;",(product_name,))
        prod_row=cur.fetchone()
        if not prod_row:
            cur.close()
            return False
        prod_id=prod_row[0]
        cur.execute("INSERT INTO sales(customer_id,product_id,quantity)VALUES(%s,%s,%s);",(cust_id,prod_id,quantity))
        cur.execute("UPDATE products SET stock=stock-%s WHERE product_id=%s;",(quantity,prod_id))

        self.conn.commit()
        cur.close()
        return True
    def add_user(self,id,username,password,role):
        hashed=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        que="INSERT INTO users(id,username,password,role)VALUES(%s,%s,%s,%s);"
        return self.execute_query(que,(id,username,hashed,role))
    def change_password(self,username,new_password):
        hashed=bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        que="UPDATE users SET password =%s WHERE username=%s;"
        return self.execute_query(que,(hashed,username))
    def get_profit_report(self):
        que="""SELECT product_name,stock,(price-buying_price),((price-buying_price)*stock) FROM products;"""
        return self.execute_query(que, fetch=True)
    def get_user(self,username):
        que=("SELECT id,username,role FROM users  WHERE username=%s;")
        out=self.execute_query(que,username)
        return out[0] if out else None
    def delete_product(self,name):
        que="DELETE FROM products WHERE product_name=%s;"
        return self.execute_query(que,(name,))
    def update_prod_name(self,name, new_name):
        que="UPDATE products SET product_name=%s WHERE product_name=%s;"
        return self.execute_query(que,(new_name, name))
    def update_stock(self,name,new_stock):
        que="UPDATE products SET stock=%s WHERE product_name=%s;"
        return self.execute_query(que,(new_stock,name))
    def update_price(self,name,new_price):
        que="UPDATE products SET price=%s WHERE product_name=%s;"
        return self.execute_query(que,(new_price,name))
    def update_bp(self,name,new_buying_price):
        que="UPDATE products SET buying_price=%s WHERE product_name=%s; "
        return self.execute_query(que,(new_buying_price,name))
    def update_all(self,name,new_price,new_stock,new_bp):
        que=("""UPDATE products SET price=%s,stock=%s,buying_price=%s WHERE product_name=%s;""")
        return self.execute_query(que,(new_price,new_stock,new_bp,name))
    def del_user(self,username):
        que=("DELETE  FROM users WHERE username=%s;")
        return self.execute_query(que, (username,))
    def update_user_role(self,username,new_role):
        que=("UPDATE users SET role=%s WHERE username=%s;")
        return self.execute_query(que,(new_role,username))


