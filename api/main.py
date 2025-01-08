import uvicorn
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import HTMLResponse, JSONResponse
from  sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from db import operations
app = FastAPI()

############### Models   ###############
class Product(BaseModel):
    name:str
    description:str 
    additional_product_ids: None | list[dict]  = None



############### Products   ###############
#  create a new product
create_prod_examples = {
    "woids": {
    "summary": "Without additional ids",
    "description": "Create a product without additional ids",
    "value": {
        "name": "Flexzilla HFZG550YW Garden Lead-In Hose 5/8 In",
        "description": "Flexzilla Garden Hose is engineered with a Flexible Hybrid Polymer that is both lightweight and durable. ",
        },
    },
    
    "wids": {
    "summary": "With additional ids",
    "description": "Create a product with additional ids. There are no checks in place to know the type of id selected(UPC, ASIN, etc). For your own sake, try to keep some consistency when naming these ids.",
    "value": {
        "name": "Flexzilla HFZG550YW Garden Lead-In Hose 5/8 In",
        "description": "Flexzilla Garden Hose is engineered with a Flexible Hybrid Polymer that is both lightweight and durable. ",
        "additional_product_ids": [{"identifier_type":"UPC", "identifier_value":"853084004477"}, {"identifier_type":"ASIN", "identifier_value":"B01NBKTPTS"},]
        },
    },
}
create_prod_responses = {
    200:{
        "description": "Product created successfully",
        "content": {
            "application/json": {
                "example": "pe376df18d1ce5dbbcb74d0c492a872be" 
            }
        }
    },
        
}
@app.post("/products",responses=create_prod_responses)
def create_new_product(product: Annotated[Product,Body(openapi_examples=create_prod_examples)]) -> str:
    """Creates a new product.

    Args:
        product (Annotated[Product,Body, optional): _description_. Defaults to create_prod_examples)].

    Returns:
        str: A unique identifier created for this product.
    """
    try:
        
        a = operations.create_new_product(name=product.name,description=product.description,additional_product_ids=product.additional_product_ids)
        return HTMLResponse(content=a)

    except IntegrityError as e:

        if 'duplicate key value violates unique constraint "products_product_name_key' in  e.args[0]:
            raise HTTPException(status_code=400,detail=f"Product `{product.name}` already exists")

        elif 'duplicate key value violates unique constraint "product_identifiers_identifier_value_key' in e.args[0]:
            raise HTTPException(status_code=400,detail="Additional product identifier(s) is already assigned to another product")







#delete a product
delete_prod_responses = {
    200:{
        "description": "Product deleted successfully",
        "content": {
            "application/json": {
                "example": "Product deleted successfully" 
            }
        }
    },
        
}
delete_prod_examples = {
    "normal": {
        "summary": "Deleting a single product",
        "description": "Delete a product by providing the product identifier. The product identifier is a unique identifier created when the product was created. This endpoint can be used to delete multiple products at the same time",
        "value": ["pe376df18d1ce5dbbcb74d0c492a872be"]
            
    },

    "multiple": {
        "summary": "Deleting multiple products",
        "description": "Delete a product by providing the product identifier. The product identifier is a unique identifier created when the product was created. This endpoint can be used to delete multiple products at the same time",
        "value": ["pe376df18d1ce5dbbcb74d0c492a872be", "pfd3c0433307c5aec6139854829f1b008", "p890e865336129d669c9a96d12cd2b9d6"]
            
    },
}
@app.delete("/products",responses=delete_prod_responses)
def delete_product(product_ids: Annotated[list[str], Body(openapi_examples=delete_prod_examples)]) -> str:

    """Deletes products.
    I do not have a way of checking if the product exists or not before it is deleted, but if it is there, it will be deleted. (Will work on this in the future)
    """
    # try:
    #     a = operations.delete_product_by_identifier(product_id)
    #     return a
    # except Exception as e:
    #     raise HTTPException(status_code=400,detail="Product does not exist")
    return HTMLResponse(content="Product deleted successfully or not")

#search product
@app.get("/products")
def search_product(search: Annotated[str, Query(min_length=3)] ) -> dict:
    """Search for a product by name.

    Args:
        name (str): The name of the product to search for.

    Returns:
        dict: A dictionary containing the product details.
    """
    # a = operations.search_product(name)
    return HTMLResponse(search)




############### Shelves    ###############
############### Containers ###############

# TODOs 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)