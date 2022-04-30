from email.policy import default
from database import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship
import enum

# By using this class on all models you get id for each of them. 
class BaseModel(Base):
    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    




class Book(BaseModel):
    __tablename__ = 'books'
    class TypeChoices(enum.Enum):
        up_to_10_days = "up_to_10_days"
        up_to_5_days = "up_to_5_days"
        up_to_2_days = "up_to_2_days"

    name = sa.Column(sa.String(100), nullable=False)
    author = sa.Column(sa.String(50), nullable=True)
    year_published = sa.Column(sa.String(4))
    type = sa.Column(sa.Enum(TypeChoices), default=TypeChoices.up_to_10_days)
    customers = relationship("Loan", back_populates="books")

   # this representation function prints the name of the rows in human lenguage 
    def __repr__(self) -> str:
        return self.name
    

    
class Customer(BaseModel):
    __tablename__ = 'customers'
    name = sa.Column(sa.String(50), nullable=False)
    city = sa.Column(sa.String(25))
    age = sa.Column(sa.Integer)
    books = relationship("Loan", back_populates="customers")

    def __repr__(self) -> str:
        return self.name



class Loan(BaseModel):
    __tablename__ = 'loans'
    customer_id = sa.Column(sa.ForeignKey("customers.id"))
    book_id = sa.Column(sa.ForeignKey("books.id"))
    loan_date = sa.Column(sa.DateTime) #2022-04-22 12:23:22
    return_date = sa.Column(sa.DateTime)
    # this is the relationship between the models combined with lines 27 and 40
    books = relationship("Book", back_populates="customers")
    customers = relationship("Customer", back_populates="books")
