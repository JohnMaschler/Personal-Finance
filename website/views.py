from flask import render_template, Blueprint, flash, request, jsonify #going to have a bunch of roots in here - spread things out
from flask_login import login_required, current_user
from .models import Transaction
from . import db
from datetime import datetime, timedelta
from sqlalchemy import extract, func
import json

"""
            <a class="nav-item nav-link" id="home" href="/home">Overview</a>
            <a class="nav-item nav-link" id="addTransaction" href="/addTransaction">Add Transaction</a>
            <a class="nav-item nav-link" href="/transactionHistory">Transaction History</a>
"""

views = Blueprint('views', __name__)

@views.route('/monthly-spending-data')
@login_required
def monthly_spending_data():
    end_date = datetime.today().date()#start and end dates for displaying data
    start_date = (end_date - timedelta(days=90))
    transactions = Transaction.query.filter(#get data from last 3 months
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date,
        Transaction.date <= end_date,
        Transaction.transaction_type == 'expense'
    ).all()
    monthly_spending = {}#store the monthly spending
    for transaction in transactions:#iterate through transactions
        date = datetime.strptime(transaction.date, '%Y-%m-%d')# get the month and year of the transaction
        month = date.month
        year = date.year
        # month = transaction.date.month#this method doesnt work
        # year = transaction.date.year
        if (year, month) in monthly_spending:# add the transaction amount to the monthly spending
            monthly_spending[(year, month)] += transaction.amount
        else:
            monthly_spending[(year, month)] = transaction.amount
    months = []#put data into lists for displaying
    spending = []
    for date, amount in sorted(monthly_spending.items()):
        year, month = date
        months.append(f'{year}-{month:02d}')
        spending.append(amount)
    return jsonify({# return the data as JSON
        'months': months,
        'spending': spending
    })

@views.route('/spending-by-category-data')
@login_required
def spending_by_category_data():
    end_date = datetime.today().date()# calculate the start and end dates of the three-month period
    start_date = (end_date - timedelta(days=90))
    spending_by_category = db.session.query(# get the user's spending by category for the last three months
        Transaction.category_id,
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,#query the data from the transaction table
        Transaction.date >= start_date,
        Transaction.date <= end_date,
        Transaction.transaction_type == 'expense'
    ).group_by(
        Transaction.category_id
    ).all()
    categories = []#put the data into lists to be displayed for the user
    spending = []
    for category, amount in spending_by_category:
        categories.append(category)
        spending.append(amount)
    return jsonify({#return the data as JSON
        'categories': categories,
        'spending': spending
    })

@views.route('/overview', methods=['GET'])
@login_required
def overview():
    return render_template('overview.html', user=current_user)


# from .models import Category

@views.route('/addTransaction', methods=['GET', 'POST'])
@login_required
def addTransaction():
    
    if request.method =='POST':
        amount = request.form.get('amount')
        transaction_type = request.form.get('transaction_type')
        category_id = request.form.get('category_id')
        date = request.form.get('date')

        if amount is None or transaction_type is None or category_id is None:
            flash("You need to fill out each field", category='error')
        else:
            new_transaction=Transaction(amount=amount,
                                        transaction_type=transaction_type,
                                        category_id=category_id,
                                        date=date,
                                        user_id=current_user.id)
            db.session.add(new_transaction)
            db.session.commit()
            flash("transaction added!", category='success')

    # user_categories = Category.query.filter_by(user_id=current_user.id).all()
    # predefined_categories = Category.query.all()
    # categories = predefined_categories #+ user_categories

    return render_template("add_transaction.html", user=current_user)

@views.route('/transactionHistory')
@login_required
def transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()#get all the transactions associated with the user
    return render_template("transaction_history.html", user=current_user, transactions=transactions)


@views.route('/delete-transaction', methods=['DELETE'])#route to delete transactions if user wants
def delete_transaction():
    transaction = json.loads(request.data)#load data
    transactionId = transaction['transactionId']
    transaction = Transaction.query.get(transactionId)#look up transaction by ID
    if transaction:
        if transaction.user_id == current_user.id:#if exists for user, delete transaction
            db.session.delete(transaction)
            db.session.commit()
            return jsonify({})



