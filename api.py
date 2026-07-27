import uuid
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from repository import DatabaseRepository


db_config = {
    "host": "localhost",
    "database": "sales_records",
    "user": "postgres",
    "password": "Ambrose@2006"   
}

rep = DatabaseRepository(db_config)

app = FastAPI(title="StockBase IMS API")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


sessions = {}   


def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    session = sessions.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return session

def require_manager(user=Depends(get_current_user)):
    if user["role"] != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")
    return user


class LoginRequest(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    stock: int
    price: float
    buying_price: float

class ProductUpdate(BaseModel):
    new_name: Optional[str] = None
    new_stock: Optional[int] = None
    new_price: Optional[float] = None
    new_buying_price: Optional[float] = None

class SaleCreate(BaseModel):
    customer_name: Optional[str] = "anonymous"
    phone: str
    product_name: str
    quantity: int

class UserCreate(BaseModel):
    id: int
    username: str
    password: str
    role: str

class RoleUpdate(BaseModel):
    new_role: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str


@app.post("/login")
def login(data: LoginRequest):
    role = rep.verify_user(data.username, data.password)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = str(uuid.uuid4())
    sessions[token] = {"username": data.username, "role": role}
    return {"token": token, "role": role, "username": data.username}

@app.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        sessions.pop(authorization.split(" ")[1], None)
    return {"message": "logged out"}


@app.get("/products")
def list_products(user=Depends(get_current_user)):
    rows = rep.get_whole_table()
    return [
        {"product_id": r[0], "product_name": r[1], "stock": r[2],
         "price": float(r[3]), "buying_price": float(r[4]) if r[4] is not None else None}
        for r in rows
    ]

@app.get("/products/{name}")
def get_product(name: str, user=Depends(get_current_user)):
    row = rep.get_product(name.lower())
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": row[0], "product_name": row[1], "stock": row[2],
            "price": float(row[3]), "buying_price": float(row[4]) if row[4] is not None else None}

@app.post("/products")
def add_product(data: ProductCreate, user=Depends(require_manager)):
    if not rep.add_product(data.name.lower(), data.stock, data.price, data.buying_price):
        raise HTTPException(status_code=400, detail="Failed to add product")
    return {"message": f"{data.name} added successfully"}

@app.put("/products/{name}")
def update_product(name: str, data: ProductUpdate, user=Depends(require_manager)):
    name = name.lower()
    if not rep.get_product(name):
        raise HTTPException(status_code=404, detail="Product not found")
    if data.new_name:
        rep.update_prod_name(name, data.new_name.lower())
        name = data.new_name.lower()
    if data.new_stock is not None:
        rep.update_stock(name, data.new_stock)
    if data.new_price is not None:
        rep.update_price(name, data.new_price)
    if data.new_buying_price is not None:
        rep.update_bp(name, data.new_buying_price)
    return {"message": "Product updated successfully"}

@app.delete("/products/{name}")
def delete_product(name: str, user=Depends(require_manager)):
    if not rep.get_product(name.lower()):
        raise HTTPException(status_code=404, detail="Product not found")
    rep.delete_product(name.lower())
    return {"message": f"{name} deleted successfully"}

@app.post("/sales")
def record_sale(data: SaleCreate, user=Depends(get_current_user)):
    if not rep.record_sale(data.customer_name, data.phone, data.product_name.lower(), data.quantity):
        raise HTTPException(status_code=400, detail="Sale failed — check product name/stock")
    return {"message": "Sale recorded successfully"}


@app.get("/profit-report")
def profit_report(user=Depends(require_manager)):
    rows = rep.get_profit_report()
    return [
        {"product_name": r[0], "stock": r[1],
         "profit_per_unit": float(r[2]), "total_profit": float(r[3])}
        for r in rows
    ]


@app.get("/users")
def list_users(user=Depends(require_manager)):
    rows = rep.get_all_users()
    return [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]

@app.get("/users/{username}")
def get_user(username: str, user=Depends(require_manager)):
    row = rep.get_user(username.lower())
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": row[0], "username": row[1], "role": row[2]}

@app.post("/users")
def add_user(data: UserCreate, user=Depends(require_manager)):
    rep.add_user(data.id, data.username.lower(), data.password, data.role.lower())
    return {"message": "User added successfully"}

@app.delete("/users/{username}")
def delete_user(username: str, user=Depends(require_manager)):
    if not rep.get_user(username.lower()):
        raise HTTPException(status_code=404, detail="User not found")
    rep.del_user(username.lower())
    return {"message": "User deleted successfully"}

@app.put("/users/{username}/role")
def update_role(username: str, data: RoleUpdate, user=Depends(require_manager)):
    if not rep.get_user(username.lower()):
        raise HTTPException(status_code=404, detail="User not found")
    rep.update_user_role(username.lower(), data.new_role.lower())
    return {"message": "Role updated successfully"}


@app.put("/me/password")
def change_password(data: PasswordChange, user=Depends(get_current_user)):
    if not rep.verify_user(user["username"], data.old_password):
        raise HTTPException(status_code=401, detail="Old password incorrect")
    rep.change_password(user["username"], data.new_password)
    return {"message": "Password changed successfully"}