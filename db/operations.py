from db.dbconfig import (
    Container, 
    Product, 
    Shelf,
    ShelfContainer,
    ContainerContent,
    engine,
)
from sqlalchemy.orm import Session
from  sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert
import secrets


############# Shelves #################

def create_new_shelf(name:str,max_capacity:int) -> str:
    """Creates a new shelf

    Args:
        name (str): The name of the shelf (should be unique)
        max_capacity (int): The capacity of the shelf (I still don't know how will I measure capacity)

    Returns:
        str: The unique identifier of the cell created
    """
    
    # generates a unique identifier like the following  's018b311e68b67759b54a08d172f04a09' 
    identifier = f"s{secrets.token_hex(16)}"


    with Session(engine) as session:

        shelf = Shelf(shelf_id = identifier, shelf_name = name, max_load_capacity = max_capacity, )
        session.add(shelf)
        session.commit()
        
    return identifier

def add_contaiers_to_shelf(containers:list[dict]):
    """Allows you to add a single or multiple containers to a shelf or shelves. \n
    NOTe: Duplicate containers in a single shelf are not allowed. A container can only be stored in one shelf at the time.

    Args:
        containers (list[dict]): A list of python dictionaries that look like the following:\n
        cont = [
            {"container_id" :"c51441d2f4cfb275bf28c3b4f3c30afce",  
            "shelf_id":"s4600c099992f81e91b0f1423aa83f7db"},
            
            {"container_id" :"cf8ddc0c29501413f16c3d5eabeb9a700",  
            "shelf_id":"s223cd0ed5e0570b800cc6578b6b451f0"},

            {"container_id" :"cdf92985c5e7b23191c7c1a2a49fd5f56",  
            "shelf_id":"s223cd0ed5e0570b800cc6578b6b451f0"},
        ]

    """
    
    try:
        #https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-bulk-insert-statements
        with Session(engine) as session:

            session.execute(insert(ShelfContainer), containers)
            session.commit()
    except IntegrityError as e:
        e.add_detail("You might be trying to add a container to a shelf that is already asigned to another shelf")
        raise e
    

def inspect_shelf_containers(shelf_id: str) -> list:
    """Looks for a shelf with the given shelf_id and returns a list of containers it is currently holding.

    Args:
        shelf_id (str): The shelf_id of the shelf.

    Returns:
        list: A list containing the container_ids inside a specific shelf.
    """
    with Session(engine) as session:
        stmt =  select(Shelf).where(Shelf.shelf_id == shelf_id)
        ex = session.execute(statement=stmt)
        results  = ex.scalar_one().shelf_containers
        result  = [x.container_id for x in results]
        
    return result


############# Containers #################

def create_new_container(name:str,max_capacity:int) -> str:
    """Creates a new container

    Args:
        name (str): The name of the container. (should be unique)
        max_capacity (int): The capacity of the container. (I still don't know how will I measure capacity)

    Returns:
        str: The unique identifier of the container created
    """
    
    # generates a unique identifier like the following  'c018b311e68b67759b54a08d172f04a09' 
    identifier = f"c{secrets.token_hex(16)}"


    with Session(engine) as session:

        container = Container(container_id = identifier, container_name = name, max_capacity = max_capacity, )
        session.add(container)
        session.commit()
        
    return identifier


def lookup_container(id: str):
    """Returns the information of the container by the provided container_id


    Args:
        id (str): _description_
    """

    
    












############# Products #################
