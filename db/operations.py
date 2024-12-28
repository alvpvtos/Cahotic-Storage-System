from db.dbconfig import (
    Container, 
    Product, 
    Shelf,
    engine,
)
from sqlalchemy.orm import Session
import secrets


############# Shelves #################

def create_new_shelf() -> str:
    """Generates a unique shelf id and places it under the "shelf" table.

    Returns:
        str: The unique identifier of the shelf created.
    """
    
    # generates a unique identifier like the following  '018b311e68b67759b54a08d172f04a09' 
    identifier = f"sh{secrets.token_hex(16)}"


    with Session(engine) as session:
        some_container = Shelf(id = identifier) 
        session.add(some_container)
        session.commit()
    
    return identifier

    


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


def lookup_container(id: str):
    """Returns the information of the container by the provided container_id


    Args:
        id (str): _description_
    """

    
    












############# Products #################
