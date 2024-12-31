from db.dbconfig import (
    Container, 
    Product, 
    Shelf,
    ShelfContainer,
    ContainerContent,
    ProductIdentifier,
    engine,
)
from sqlalchemy.orm import Session
from  sqlalchemy.exc import IntegrityError
from sqlalchemy import (
    func,
    select,
    delete,
    insert,
)
import secrets
import json


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
    
def unbind_containers_from_shelfs(containers:list[str]):
    """Unbinds or "removes" a single or multiple containers from a shelf.\n
    Multiple containers can be removed at the same time from the same or different shelf.

    Args:
        containers (list[str]): A list of containers to be unbound from a shelf. ex:\n
        cont = [
            "c51441d2f4cfb275bf28c3b4f3c30afce",  
            "cf8ddc0c29501413f16c3d5eabeb9a700",  
            "cdf92985c5e7b23191c7c1a2a49fd5f56",  
        ]
    """

    # https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-update-and-delete-with-custom-where-criteria
    with Session(engine) as session:

        stmt = delete(ShelfContainer).where(ShelfContainer.container_id.in_(containers))
        session.execute(stmt)
        session.commit()


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

def delete_shelfs(shelf_ids:list[str]):
    """Delete a single or multiple shelves.

    Args:
        shelf_ids (list[str]): A list of shelves ids to be deleted.\n
        Example:\n
        sh = [
            "s51441d2f4cfb275bf28c3b4f3c30afce",  
            "sf8ddc0c29501413f16c3d5eabeb9a700",  
            "sdf92985c5e7b23191c7c1a2a49fd5f56",  
        ]
    """
    # https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-update-and-delete-with-custom-where-criteria
    with Session(engine) as session:
        try:
            stmt = delete(Shelf).where(Shelf.shelf_id.in_(shelf_ids))
            session.execute(stmt)
            session.commit()
        except IntegrityError as e:
            e.add_detail(
                "You might be trying to delete a shelf that  has  containers bound to it.\nRemove that container(s) from shelf and try again"
            )
            raise(e)

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
#nOTE create functin that modifies additional_product_ids from a product

def create_new_product(name:str, description:str, additional_product_ids: None | list[dict] = None ) -> str:
    """Creates a new product.

    Args:
        name (str): The desired name for the product.
        description (str): The desired description for the product.\n
        additional_product_ids (list[dict]): Optional argument | Used to store additional product codes such as ASINs or UPCs.\n 
        If used, pass a list of dictionaries such as the following:\n
        pc = [
            {"identifier_type":"UPC", "identifier_value":"853084004477"},
            {"identifier_type":"ASIN", "identifier_value":"B01NBKTPTS"},
            {"identifier_type":"GTIN", "identifier_value":"00853084004477"},
        ]      

    Returns:
        str: The unique identifier created for this product.
    """

    identifier = f"p{secrets.token_hex(16)}"

    if additional_product_ids:

        # Create a list of ProductIdentifier objects to pass into Product(identifiers)
        ids = []
        for i in additional_product_ids:
            id = ProductIdentifier(identifier_type= i["identifier_type"], identifier_value= i["identifier_value"] )
            ids.append(id)

        with Session(engine) as session:

            try:

                container = Product(product_id=identifier, product_name=name, description=description, additional_identifiers=ids)
                session.add(container)
                session.commit()
            
                return identifier

            except IntegrityError as e:
                e.add_detail("You might be trying to add an additinal_identifier to this product that has already being assigned to another product")
                raise e

    else:
        with Session(engine) as session:
            try:
                
                container = Product(product_id=identifier, product_name=name, description=description)
                session.add(container)
                session.commit()

                return identifier

            except IntegrityError as e:
                e.add_detail("You might be trying to create a product that already exists")
                raise e
    
    
def convert_product_object_to_json(product_object:Product) -> str:
    # work in progress, try a with statement with an sqlalchemy.orm.Session if it does not work.
    """This function will take a db.dbconfig.Product object and convert it to a JSON string.

    Args:
        product_object (Product):A db.dbconfig.Product object.

    Returns:
        str: A JSON string.
    """
    
    d = {
        'name': product_object.product_name,
        'description': product_object.description,
        'product_id': product_object.product_id,
        # this line basically creates a list of dicts if our object has additional ids in it, if not, it returns an empty list.
        # 'additional_ids': list(map(lambda add_id: {"identifier_type":add_id.identifier_type,"value":add_id.identifier_value},product.additional_identifiers)),
        'additional_ids': [{"identifier_type":x.identifier_type, "value":x.identifier_value} for x in product_object.additional_identifiers],
        'date_added': product_object.created_at.isoformat(),
    }
    result = json.dumps(d,indent=4)

    return result

def search_product_by_product_id(product_id:str)-> list[dict] | None:
    """ Will try to find the product by product_id, you can pass an entire product_id or part of it. (Useful for active search)

    Args:
        product_id (str): Example: "pe376df18d1ce5dbbcb74d0c492a872be" or "p"

    Returns:
        list[dict]None: A list of products found
    """

    with Session(engine) as session:

        results = session.query(Product).filter(
            (Product.product_id == product_id) |  # Exact match
            (Product.product_id.like(f"%{product_id}%"))  # Partial match (contains)
        )

        matches = [convert_product_object_to_json(product) for product in results]
            

    return matches


def search_product_by_name(product_name:str)-> list[dict] | None:
    """ Will try to find the product by name, you can pass the full name of the product or part of it. (Useful for active search)

    Args:
        product_id (str): Example: "Pliers" or "pli"

    Returns:
        list[dict]None: A list of products found
    """

    with Session(engine) as session:

        # sqlalchemy.func
        results = session.query(Product).filter(
            (func.lower(Product.product_name) == product_name.lower()) |  # Exact match
            (func.lower(Product.product_name).like(f"%{product_name.lower()}%"))  # Partial match (contains)
        )

        matches = [convert_product_object_to_json(product) for product in results]
            

    return matches




def delete_product_by_identifier(products:list[str])-> str | None:
    """Deletes a single  or multiple products from the db.

    Args:
        product_id (list[str]): A list of unique product ids. Example ["pc85ba29f7bccdb4fc9d877da9786023b","pv34.."]

    Returns:
        str: A list of pro
    """
    with Session(engine) as session:
        stmt = delete(Product).where(Product.product_id.in_(products))
        session.execute(stmt)
        session.commit()