from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, func, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, backref

DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)

# --- Base Class ---
class Base(DeclarativeBase):
    pass

# --- Products Table ---
class Product(Base):
    """
    A table that stores products and information about them.
    """
    __tablename__ = 'products'
    
    product_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # A list of additional identifiers 
    # Allows us to call Products.identifiers and get a list of identifiers if any are set.
    additional_identifiers: Mapped[list['ProductIdentifier']] = relationship(
        back_populates='product',
        cascade="all, delete-orphan" # should allow you to delete the ProductIdentifiers assosiated with it.
    )
# --- Product Identifiers Table ---
class ProductIdentifier(Base):
    """
    A table to store product identifiers such as UPCs, ASINs, etc.
    """
    __tablename__ = 'product_identifiers'
    
    identifier_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.product_id',ondelete="CASCADE"), nullable=False)
    identifier_type: Mapped[str] = mapped_column(String(20), nullable=False)
    identifier_value: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    product: Mapped['Product'] = relationship(back_populates='additional_identifiers')

# --- Containers Table ---
class Container(Base):
    """
    A table that stores containers and information about them.
    """
    __tablename__ = 'containers'
    
    container_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    container_name: Mapped[str] = mapped_column(String, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    contents: Mapped[list['ContainerContent']] = relationship(back_populates='container')


# --- ContainerProducts Table ---

class ContainerContent(Base):
    """Junction table between containers and products.\n
    This table makes it possible to "store" products in a container.
    """
    __tablename__ = 'container_contents'
    
    content_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    container_id: Mapped[str] = mapped_column(ForeignKey('containers.container_id'), nullable=False)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.product_id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    container: Mapped['Container'] = relationship(back_populates='contents')
    product: Mapped['Product'] = relationship()



# --- Shelves Table ---
class Shelf(Base):
    """
    A table that stores shelves and information about them.
    """
    __tablename__ = 'shelves'
    
    shelf_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    shelf_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    max_load_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    shelf_containers: Mapped[list['ShelfContainer']] = relationship(back_populates='shelf')

# --- Container Contents Table ---

# --- Shelf Containers Table ---
class ShelfContainer(Base):
    """Junction table between containers and shelves.\n
    This table makes it possible to "store" containers in a shelf.
    """
    __tablename__ = 'shelf_containers'
    
    shelf_container_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    shelf_id: Mapped[str] = mapped_column(ForeignKey('shelves.shelf_id'), nullable=False)
    container_id: Mapped[str] = mapped_column(ForeignKey('containers.container_id'), nullable=False, unique=True)
    placed_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    shelf: Mapped['Shelf'] = relationship(back_populates='shelf_containers')
    container: Mapped['Container'] = relationship()

Base.metadata.create_all(engine)
