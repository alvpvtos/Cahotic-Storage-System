from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, func, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase



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
    
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

# --- Containers Table ---
class Container(Base):

    """
    A table that stores containers and information about them.
    """
    __tablename__ = 'containers'
    
    container_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    container_name: Mapped[str] = mapped_column(String, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    contents: Mapped[list['ContainerContent']] = relationship(back_populates='container')



# --- Shelves Table ---
class Shelf(Base):

    """
    A table that stores shelves and information about them.
    """
    __tablename__ = 'shelves'
    
    shelf_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    shelf_name: Mapped[str] = mapped_column(String, nullable=False)
    max_load_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    shelf_containers: Mapped[list['ShelfContainer']] = relationship(back_populates='shelf')

# --- Container Contents Table ---
class ContainerContent(Base):
    """Junction table betwen containers and products.\n
    This table makes it possible to "store" products in a container.
    """

    __tablename__ = 'container_contents'
    
    content_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    container_id: Mapped[int] = mapped_column(ForeignKey('containers.container_id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    container: Mapped['Container'] = relationship(back_populates='contents')
    product: Mapped['Product'] = relationship()

# --- Shelf Containers Table ---
class ShelfContainer(Base):

    """Junction table betwen containers and shelves.\n
    This table makes it possible to "store" containers in a shelf.

    """
    __tablename__ = 'shelf_containers'
    
    shelf_container_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    shelf_id: Mapped[int] = mapped_column(ForeignKey('shelves.shelf_id'), nullable=False)
    container_id: Mapped[int] = mapped_column(ForeignKey('containers.container_id'), nullable=False)
    placed_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    shelf: Mapped['Shelf'] = relationship(back_populates='shelf_containers')
    container: Mapped['Container'] = relationship()

# # --- Movements Table --- (to be implemented at a later stage of the project)
# class Movement(Base):
#     __tablename__ = 'movements'
    
#     movement_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'), nullable=False)
#     from_container_id: Mapped[int | None] = mapped_column(ForeignKey('containers.container_id'), nullable=True)
#     to_container_id: Mapped[int | None] = mapped_column(ForeignKey('containers.container_id'), nullable=True)
#     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
#     moved_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

#     product: Mapped['Product'] = relationship()
#     from_container: Mapped['Container'] = relationship(foreign_keys=[from_container_id])
#     to_container: Mapped['Container'] = relationship(foreign_keys=[to_container_id])


# Synchronous engine (replace with async if needed)

Base.metadata.create_all(engine)