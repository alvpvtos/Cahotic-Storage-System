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



class AdditionalIds(BaseModel):
    identifier_type: str
    identifier_value: str
class Product_Search_Result(BaseModel):
    name: str
    description: str
    product_id: int
    additional_ids : None | list[AdditionalIds]
    date_added: str

search_prod_responses = {
    200:{
        "description": "Successfull search",
        "content": {
            "application/json": {
                "example":     [{
                    "name": "Flexzilla HFZG550YW Garden Lead-In Hose 5/8 In",
                    "description": "Flexzilla Garden Hose is engineered with a Flexible Hybrid Polymer that is both lightweight and durable. ",
                    "product_id": "p890e865336129d669c9a96d12cd2b9d6",
                    "additional_ids": [
                        {
                            "identifier_type": "UPC",
                            "identifier_value": "853084004477"
                        },
                        {
                            "identifier_type": "ASIN",
                            "identifier_value": "B01NBKTPTS"
                        }
                    ],
                    "date_added": "2025-01-08T03:43:33.850485", 
                }, ]
            }
        }
    },
        
}
#search product
@app.get("/products",responses=search_prod_responses)
def search_product(search: Annotated[str, Query(min_length=3, )] ) -> list[Product_Search_Result]:
    """Search for a product. 
    You can search for a product by name or unique id. The search is case-insensitive and will return a list of products that match the search query.

    """
    results = []
    name_results = operations.search_product_by_name(search)
    id_results = operations.search_product_by_product_id(search)

    results.extend(name_results)
    results.extend(id_results)

    if results:
        return JSONResponse(results)

    raise HTTPException(
        status_code=404,
        detail=f"The query `{search}` did not return any results"
    )


############### Containers ###############

create_cont_responses = {
    200:{
        "description": "Container created successfully",
        "content": {
            "application/json": {
                "example":  [ 
                    "cd0e1aa62028e812793af5d1703759fa8"
                ]
            }
        }
    },
        
}
@app.post("/container", responses=create_cont_responses)
def crete_container(
    name: str = Query(..., min_length=3, max_length=50, description="Name of the container"),
    max_capacity: int = Query(..., gt=0, description="Maximum capacity of the container. (There is no real use for this yet, I have not thought of a way to use it.)"),
    quantity: int = Query(..., gt=0,description="Number of containers to create")
):
    """ Creates a single or multiple containers with the characteristics provided.

    """
    new_containers = operations.create_new_container(name=name, max_capacity=max_capacity, quantity=quantity)
    # return f"Container {new_container} was successfully created"
    return  new_containers


delete_prod_examples = {
    "normal": {
        "summary": "Deleting a single container",
        "description": "Delete a product by providing the product identifier. The product identifier is a unique identifier created when the product was created. This endpoint can be used to delete multiple products at the same time",
        "value": ["ce376df18d1ce5dbbcb74d0c492a872be"]
            
    },

    "multiple": {
        "summary": "Deleting multiple containers",
        "description": "Delete a product by providing the product identifier. The product identifier is a unique identifier created when the product was created. This endpoint can be used to delete multiple products at the same time",
        "value": ["ce376df18d1ce5dbbcb74d0c492a872be", "cfd3c0433307c5aec6139854829f1b008", "c890e865336129d669c9a96d12cd2b9d6"]
            
    },
}

delete_cont_responses = {
    200:{
        "description": "Container created successfully",
        "content": {
            "application/json": {
                "example":  [ 
                    "cd0e1aa62028e812793af5d1703759fa8"
                ]
            }
        }
    },
        
}
@app.delete("/containers", responses=delete_cont_responses)
def delete_container(container_ids: Annotated[list[str], Body(openapi_examples=delete_prod_examples)]):
    """Deletes a single or multiple containers.
    """
    container = operations.delete_container(container_ids)
    return container_ids



# @app.post("/containers/add_product_to_container")
# def add_product_to_container(addition: ProductContainers):


############### Shelves    ###############


# TODOs 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)