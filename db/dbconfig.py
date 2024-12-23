from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint
)
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,  DeclarativeBase, Mapped, mapped_column 



DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"

# Synchronous engine (replace with async if needed)
engine = create_engine(DATABASE_URL)

# base class to create db models
class Base(DeclarativeBase):
    pass

class Container(Base):
    __tablename__ = 'container'
    id: Mapped[str] = mapped_column(String(333), primary_key=True)


class Product(Base):
    __tablename__ = 'product'
    
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    product_identifier: Mapped[str] = mapped_column(String(333), primary_key=True)
    identifier_type: Mapped[str] = mapped_column(String(255))
    
    __table_args__ = (
        UniqueConstraint('product_identifier', name='unique_identifier_for_product_code'),
    )


class Shelf(Base):
    __tablename__ = 'shelf'
    
    shelf_id: Mapped[str] = mapped_column(String(333), primary_key=True)

# Establishing relationship to ContainerProducts in Product and Container for ORM navigation
Product.container_products = relationship("ContainerProducts", back_populates="product")
Container.container_products = relationship("ContainerProducts", back_populates="container")

class ContainerProducts(Base):
    __tablename__ = 'container_products'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[str] =  mapped_column(ForeignKey('product.product_identifier'))
    container_id: Mapped[str] = mapped_column(ForeignKey('container.id'))
    count: Mapped[int] = mapped_column(Integer)

    product = relationship("Product", back_populates="container_products")
    container = relationship("Container", back_populates="container_products")

    __table_args__ = {'comment': 'This table is a junction table that is in charge of keeping track of which products are stored in which containers'}


class ShelfContainers(Base):
    __tablename__ = 'shelf_containers'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    container_id: Mapped[str] = mapped_column(String(333), ForeignKey('container.id'))
    shelf_id: Mapped[str] = mapped_column(String(333), ForeignKey('shelf.shelf_id'))

    container = relationship("Container", backref="shelf_containers")
    shelf = relationship("Shelf", backref="shelf_containers")
    
    __table_args__ = (
        UniqueConstraint('container_id', name='shelf_containers_container_id_key'),
        {'comment': 'Links the container and shelf tables to keep track of how many containers are there in a shelf, etc.'}
    )


Base.metadata.create_all(engine)