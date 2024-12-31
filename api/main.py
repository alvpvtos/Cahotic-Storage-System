
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db.operations import (
    create_new_product, 
    search_product_by_product_id, 
    search_product_by_name, 

    convert_product_object_to_json,   
    create_new_container, 
    unbind_containers_from_shelfs, 

    delete_shelfs, 
    create_new_shelf, 
    inspect_shelf_containers, 
    add_contaiers_to_shelf
)

app = FastAPI()


############### Products   ###############
@app.post("/products/{product_identifier}")
def create_new_product(product: Product):
    pass
############### Shelves    ###############
############### Containers ###############