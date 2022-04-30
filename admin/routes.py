from flask import Blueprint, render_template, abort, request, redirect, url_for
from .forms import AddCustomerForm, AddBookForm, AddLoanForm
import datetime
from main.models import Customer, Loan, Book
from database import db_session
admin = Blueprint('admin', __name__)

# In this Module you'll find all the routes to the hmtl files besides main


@admin.route('/add-customer', methods=["GET", "POST"])
def add_customer():
    form = AddCustomerForm()

    if request.method == "POST":

        if form.validate_on_submit():

            new_customer = Customer()
            new_customer.name = request.form.get("name")
            new_customer.city = request.form.get("city")
            new_customer.age = request.form.get("age")

            db_session.add(new_customer)
            db_session.commit()
            return redirect(url_for("admin.list_customers"))

    return render_template(f'pages/admin/add_customer.html', form=form)

# This url shows you all the books in the library store and also can be filter by using the search feature


@admin.route("/list-customers", methods=['GET'])
def list_customers():

    search = request.args.get('q', type=str)

    if search is None:

        customers_query = db_session.query(Customer).all()
    else:
        customers_query = db_session.query(Customer).filter(
            Customer.name.like("%" + search + "%")).all()

    return render_template("pages/admin/list-customers.html", customers=customers_query)


@admin.route("/delete-customer/<id>", methods=["GET"])
def delete_customer(id):

    customer = db_session.query(Customer).filter_by(id=id).first()
    db_session.delete(customer)
    db_session.commit()
    return redirect(url_for("admin.list_customers"))


@admin.route("/add-book", methods=['POST', 'GET'])
def add_book():

    form = AddBookForm()

    if request.method == "POST":

        if form.validate_on_submit():

            new_book = Book()
            new_book.name = request.form.get("name")
            new_book.author = request.form.get("author")
            new_book.year_published = request.form.get("year_published")
            new_book.type = request.form.get("type")

            db_session.add(new_book)
            db_session.commit()

            return redirect(url_for("admin.list_books"))

    return render_template("pages/admin/add_book.html", form=form)


@admin.route("/list-books", methods=['GET'])
def list_books():

    search = request.args.get('q', type=str)

    if search is None:

        books_query = db_session.query(Book).all()
    else:
        books_query = db_session.query(Book).filter(
            Book.name.like("%" + search + "%")).all()

    return render_template("pages/admin/list-books.html", books=books_query)


@admin.route("/delete-book/<id>", methods=["GET"])
def delete_book(id):

    book = db_session.query(Book).filter_by(id=id).first()
    db_session.delete(book)
    db_session.commit()
    return redirect(url_for("admin.list_books"))


@admin.route("/add-load", methods=['POST', 'GET'])
def add_loan():

    form = AddLoanForm()

    if request.method == "POST":

        if form.validate_on_submit():

            book_id = request.form.get("book")
            customer_id = request.form.get("customer")

            target_book = db_session.query(Book).filter_by(id=book_id).first()

            if target_book.type.value == "up_to_10_days":
                days = 10
            elif target_book.type.value == "up_to_5_days":
                days = 5
            elif target_book.type.value == "up_to_2_days":
                days = 2

            current_time = datetime.datetime.today()
            return_time = datetime.datetime.today() + datetime.timedelta(days=days)

            new_loan = Loan()

            new_loan.customer_id = customer_id
            new_loan.book_id = book_id
            new_loan.loan_date = current_time
            new_loan.return_date = return_time

            db_session.add(new_loan)
            db_session.commit()
            return redirect(url_for("admin.list_loans"))

    return render_template("pages/admin/add_loan.html", form=form)


@admin.route("/list-loans", methods=['GET'])
def list_loans():

    loan_query = db_session.query(Loan).all()

    return render_template("pages/admin/list-loans.html", loans=loan_query)


@admin.route("/list-loans/late", methods=['GET'])
def list_late_loans():
    # this allows us to filter the loans in case we only want to check the late ones
    loan_query = db_session.query(Loan).filter(
        Loan.return_date < datetime.datetime.today())

    return render_template("pages/admin/list-loans.html", loans=loan_query)
