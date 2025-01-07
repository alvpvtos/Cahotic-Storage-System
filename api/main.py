from typing import Annotated
from fastapi import FastAPI, HTTPException, Body 
from pydantic import BaseModel, Field
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

############### Models   ###############
class Product(BaseModel):
    name:str = Field(..., example="Garden Hose", description="The name of your product")
    description:str = Field(..., example="This is a garden hose, used to water your plants", description="The description of your product")
    additional_product_ids: None | list[dict] = Field(default=None, description="A list of additional product IDs for your product, " )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Flexzilla HFZG550YW Garden Lead-In Hose 5/8 In. x 50 ft, Heavy Duty, Lightweight, Drinking Water Safe ",
                    "description": "Flexzilla Garden Hose is engineered with a Flexible Hybrid Polymer that is both lightweight and durable. This premium hose redefines flexibility and is easy to maneuver around your yard. Flexzilla Garden Hose has zero memory which allows the hose to lay flat and ensures that sprinklers stay put without twisting.",
                    "additional_product_ids": [{"UPC":"092329591512","ASIN":"B003TFE7ZM"}]
                }
            ]
        }
    }



############### Products   ###############
#  create a new product
@app.post("/products/new")
def create_new_product(product: Annotated[Product,Body()]) -> str:
    return product.name

############### Shelves    ###############
############### Containers ###############