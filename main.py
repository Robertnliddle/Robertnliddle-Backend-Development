from flask import Flask
from flask import render_template
from flask import request
from manager import manager

from database import (
    load_balance,
    load_history,
    load_warehouse,
    save_balance,
    save_history,
    save_warehouse
)


app = Flask(__name__)


@app.route("/", methods=["GET, POST"])
@app.route("/balance", methods=["GET, POST"])
def index():
    account = load_balance()
    inventory = load_warehouse()
    history = load_history()
    if request.method == "POST":
        actions = request.form.get("action")
        value = int(request.form.get("value", 0))

        inventory, balance, history = manager.execute("balance", account, history, inventory,
                                                      actions=actions, value=value)
        save_balance(account)
        save_history(history)
        save_warehouse(inventory)
    return render_template("index.html", account=account, inventory=inventory)


@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    if request.method == "POST":
        inventory = load_warehouse()
        account = load_balance()
        history = load_history()

        name = request.form.get("name")
        price = request.form.get("price")
        count = request.form.get("count")
        account, inventory, history = manager.execute("purchase", account, inventory, history, product_name=name,
                                                      price=price, quantity=count)
        save_warehouse(inventory)
        save_balance(account)
        save_history(history)

    return render_template('purchase.html')


@app.route("/sale", methods=["GET", "POST"])
def sales():
    inventory = load_warehouse()
    account = load_balance()
    history = load_history()
    if request.method == "POST":

        name = request.form.get("name")
        price = request.form.get("price")
        count = request.form.get("count")

        account, inventory, history = manager.execute("purchase", account, inventory, history, product_name=name,
                                                      price=price, quantity=count)

        save_warehouse(inventory)
        save_balance(account)
        save_history(history)

    return render_template("sales.html", inventory=inventory)


@app.route("/balance", methods=["GET', 'POST"])
def balance():
    return render_template('balance.html')


@app.route("/history")
def history():
    history = load_history()
    return render_template("history.html", history=history)