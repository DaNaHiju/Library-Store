from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from database import db_session
from main.models import Book, Loan, Customer

# Here I used wtforms to create the forms that are used in the GUI to add customers, book and loans


class AddCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])


class AddBookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired()])
    type = SelectField(choices=[("up_to_10_days", "Up to 10 days"), (
        "up_to_5_days", "Up to 5 days"), ("up_to_2_days", "Up to 2 days")])


class AddLoanForm(FlaskForm):

    # since the loans model is the relationship between the other two models here we need to ass a query to each of them, this way they will appear as options in the GUI
    def list_books_query():
        return db_session.query(Book).all()

    def list_customers_query():
        return db_session.query(Customer).all()

    book = QuerySelectField('Book',
                            validators=[DataRequired()],
                            query_factory=list_books_query)
    customer = QuerySelectField('Customer',
                                validators=[DataRequired()],
                                query_factory=list_customers_query)
