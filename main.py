from flask import Flask
from flask import render_template
from flask import request

from database import (
    load_account,
    load_history,
    load_inventory,
    save_account,
    save_history,
    save_inventory
)


app = Flask(__name__)


balance = 1000


@app.route('/')
def index():
    account = load_account()
    inventory = load_inventory()
    return render_template("index.html", account=account, inventory=inventory)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        inventory = load_inventory()
        account = load_account()
        history = load_history()

        name = request.form.get("name")
        price = request.form.get("price")
        count = request.form.get("count")
        account, inventory, history = manager.execute("purchase", name, price, count)

        save_inventory(inventory)
        save_account(account)
        save_history(history)

    return render_template('purchase.html')


@app.route('/sale', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        print(request.form)
    return render_template('sale.html')


@app.route('/balance', methods=['GET', 'POST'])
def balance():
    if request.method == 'POST':
        return render_template('balance.html')


@app.route('/history')
def history():
    history = load_history()
    return render_template("history.html", history)