from fastapi import FastAPI,Depends
from models import Product
from database import sessionlocal,engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000/"]
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # No trailing slash
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods: GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allow all headers
)

database_models.Base.metadata.create_all(bind=engine)

products=[
     Product(id=15,name="Vivo",description="Good",price=12232,quantity=1) ,
      Product(id=16,name="redmi",description="Good",price=12232,quantity=1) ,
       Product(id=17,name="Vivo",description="Good",price=12232,quantity=1)  
]
# def init_db():
#     db = sessionlocal()
#     try:
#         for product in products:
#             db.add(database_models.Product(**product.model_dump()))
#         db.commit()
#         print("Products inserted successfully.")
#     except Exception as e:
#         db.rollback()
#         print(" Error inserting products:", e)
#     finally:
#         db.close()

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db=sessionlocal()
    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()


init_db() 
@app.get("/")   
def greet():
    return "Welcome To LM" 

@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):  

    db_product=db.query(database_models.Product).all()
    return db_product
# Manual frtch by id from lsit
# @app.get("/product/{id}")
# def get_product_byID(id:int):
#     for product in products:
#         if product.id == id:
#             return product.__dict__
#     return -1

# /fetch by specific id in databse
@app.get("/products/{id}")
def get_product_byID(id:int,db:Session=Depends(get_db)):
    dbproduct=db.query(database_models.Product).filter(database_models.Product.id==id).first()    
    if dbproduct:
        return dbproduct
    return "Product Not Found"

# /insert  a new product Manually
# @app.post("/product")
# def addproduct(product:Product):
#     products.append(product)
#     return product

# Add product in db  Works Okkk
@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

# Update a product  Manually
# @app.put("/product")
# def update_product(id:int,product:Product,):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i]=product
#             return "Product Added Sucessfully....!"
    # return "No Product Found !"


# Update a product FROM DB
@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    
    dbproduct=db.query(database_models.Product).filter(database_models.Product.id==id).first() 
    if dbproduct:
        dbproduct.name=product.name
        dbproduct.description=product.description
        dbproduct.price=product.price
        dbproduct.quantity=product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No Product Found !"


# /Delete Product MANUALLY
# @app.delete("/product")
# def delete_Product(id:int):
#     for i in range(len(products)):
#         if products[i].id==id:
#             del products[i]
#             return "Deleted"
#     return "element not found"


# dELETE product FROM DB OKKK
@app.delete("/products/{id}")
def delete_Product(id:int,db:Session=Depends(get_db)):
   dbproduct=db.query(database_models.Product).filter(database_models.Product.id==id).first() 
   if dbproduct:
       db.delete(dbproduct)
       db.commit()
       return "Deletion Successfully"
   else:
       return "Element not found"
