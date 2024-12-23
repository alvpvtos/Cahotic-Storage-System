from db.dbconfig import (
    Container, 
    Product, 
    Shelf,
    engine,
)
from sqlalchemy.orm import Session
import secrets



############# Containers #################

def create_new_container() -> str:
    """Generates a unique container id and places it under the "container" table.

    Returns:
        str: The unique identifier of the container created.
    """
    
    # generates a unique identifier like the following  '018b311e68b67759b54a08d172f04a09' 
    identifier = secrets.token_hex(16)


    with Session(engine) as session:
        some_container = Container(id = identifier) 
        session.add(some_container)
        session.commit()
    
    return identifier












############# Products #################
############# Shelves #################