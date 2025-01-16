import uvicorn
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.responses import HTMLResponse, JSONResponse
from  sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from db import operations
app = FastAPI()

############### Models   ###############
# request body of a product
class Product(BaseModel):
    name:str
    description:str 
    additional_product_ids: None | list[dict]  = None


class AdditionalIds(BaseModel):
    identifier_type: str
    identifier_value: str

# response body of a prouct search
class Product_Search_Result(BaseModel):
    name: str
    description: str
    product_id: int
    additional_ids : None | list[AdditionalIds]
    date_added: str

#adding a container to a shelf
class Container_Shelf(BaseModel):
    container_id: str
    shelf_id: str
    

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

#inspec container contents

@app.get("/containers")
def inspect_container(container_id: Annotated[str, Query(..., min_length=3, max_length=50, description="The unique identifier of the container")]) -> list[dict]:


    """Inspect the contents of a container.


    """
    result = operations.inspect_container(container_id)

    return result




@app.post("/containers/product")
def add_product_to_container(
    product_id : str = Query(..., min_length=3, max_length=50, description="The unique identifier of the product"),
    container_id: str = Query(..., min_length=3, max_length=50, description="The unique identifier of the container"),
    count: int = Query(..., gt=0, description="Number of products to add to the container")
):
    """Add a product to a container.
    """
    operations.add_product_to_container(product_id, container_id, count)
    return f"Product {product_id} added to container {container_id}"



@app.delete("/containers/product")
def remove_product_from_container(
    product_id : str = Query(..., min_length=3, max_length=50, description="The unique identifier of the product"),
    container_id : str = Query(...,  min_length=3, max_length=50, description="The unique identifier of the container"),
    quantity : int = Query(..., gt=0, description="Quantity of the product to remove from  container"),
    
):
    # the id of the container is needed in order to know where to remove the product from.

    """Remove a product from a container. Only the product id is required.
    """
    try:
        
        operations.remove_product_from_container(product_id=product_id, container_id=container_id, quantity=quantity)
        return f"Product {product_id} removed from container"

    except ValueError as e :
        raise HTTPException(status_code=400, detail=e.args[0])
        
    

############### Shelves    ###############

@app.post("/shelves")
def create_shelf(
    name: str = Query(..., min_length=3, max_length=50, description="Name of the shelf"),
    max_capacity: int = Query(..., gt=0, description="Maximum capacity of the shelf. (There is no real use for this yet, I have not thought of a way to use it.)"),
    # quantity: int = Query(..., gt=0,description="Number of shelves to create") (to be implemented)

):
    """ Creates a single shelf.

    """
    new_shelf = operations.create_new_shelf(name=name, max_capacity=max_capacity)
    return  new_shelf

# delete shelf

delete_shelf_examples = {
    "Single": {
    "summary": "Deleting a single shelf",
    "description": "Deleting a single shelf",
    "value": ["se376df18d1ce5dbbcb74d0c492a872be"],
    },

    "Multiple": {
    "summary": "Deleting multiple shelves",
    "description": "Deleting multiple shelves",
    "value": ["se376df18d1ce5dbbcb74d0c492a872be","s4600c099992f81e91b0f1423aa83f7db", "s4600c099992f81e91b0f1423aa83f7db"],
    }
}

@app.delete("/shelves")
def delete_shelves(shelf_id:  Annotated[list[str], Body(description="A list of unique shelf identifiers", openapi_examples=delete_shelf_examples)]):

    """Deletes a single  or multiple shelves.
    """

    # error handling when shelf has containers in it to be implemented

    operations.delete_shelves(shelf_id)
    # return f"Shelf {shelf_id} deleted successfully"
    return shelf_id

#inspect shelf

@app.get("/shelves")
def inspect_shelf(shelf_id =  Query(description="The id of the container to be searched")):
    contents = operations.inspect_shelf_containers(shelf_id)
    return {"containers":contents}


#add container to shelf

add_container_examples = {
    "single": {
    "summary": "Adding multiple products to a single shelf",
    "description": "Adding multiple products to a single shelf",
    "value": [
        {"container_id" :"c51441d2f4cfb275bf28c3b4f3c30afce",  
        "shelf_id":"s4600c099992f81e91b0f1423aa83f7db"},
        
        {"container_id" :"cf8ddc0c29501413f16c3d5eabeb9a700",  
        "shelf_id":"s4600c099992f81e91b0f1423aa83f7db"},

        {"container_id" :"cdf92985c5e7b23191c7c1a2a49fd5f56",  
        "shelf_id":"s4600c099992f81e91b0f1423aa83f7db"},
        ],
    },
    
    "multiple": {
    "summary": "Adding multiple products to multiple shelves",
    "description": "Adding multiple products to multiple shelves",
    "value": [
        {"container_id" :"c51441d2f4cfb275bf28c3b4f3c30afce",  
        "shelf_id":"s4600c099992f81e91b0f1423aa83f7db"},
        
        {"container_id" :"cf8ddc0c29501413f16c3d5eabeb9a700",  
        "shelf_id":"s223cd0ed5e0570b800cc6578b6b451f0"},

        {"container_id" :"cdf92985c5e7b23191c7c1a2a49fd5f56",  
        "shelf_id":"s223cd0ed5e0570b800cc6578b6b451f0"}
        ],
    },
}
@app.post("/shelves/container")
def add_containers_to_shelves(containers: Annotated[list[Container_Shelf], Body(description="A list of containers to add to the shelf",openapi_examples=add_container_examples)]):   
    """Adds containers to shelves.
    """
    operations.add_containers_to_shelf(containers)
    return {"message": "Containers added to shelf"}



# remove container from shelf

remove_container_examples = {
    "Normal": {
    "summary": "Removing a container from a shelf",
    "description": "Remove a single or multiple containers from a shelf. The shelf id is not needed since one container should only be bound to a single shelf",
    "value": [
        "c51441d2f4cfb275bf28c3b4f3c30afce",
        "cf8ddc0c29501413f16c3d5eabeb9a700"
        ],
    },
}
@app.delete("/shelves/container")
def remove_container_from_shelf(
    containers:  Annotated[list[str], Body(description="A list of container ids",openapi_examples=remove_container_examples)],
):
    """Removes a container from a shelf.
    """
    operations.unbind_containers_from_shelf(containers)

    return {"message": "Container removed from shelf"}



#     return
# TODOs 

if __name__ == "__main__":
    uvicorn.run(app, port=8000)