from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_transaction, get_transactions, delete_transaction

app = Flask(__name__)

@app.route('/')
def index():
    transactions = get_transactions()
    balance = sum(t[1] if t[4] == 'income' else -t[1] for t in transactions)
    return render_template('index.html', transactions=transactions, balance=balance)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        type = request.form['type']
        add_transaction(amount, category, description, type)
        return redirect(url_for('index'))
    return render_template('add_transaction.html')


@app.route('/delete/<int:id>')
def delete(id):
    try:
        delete_transaction(id)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Fehler beim Löschen: {e}")  # Loggt den Fehler in die Konsole
        return "Fehler beim Löschen", 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)