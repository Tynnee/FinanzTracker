from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_transaction, get_transactions, delete_transaction

app = Flask(__name__)

@app.route('/')
def index():
    transactions = get_transactions()
    balance = sum(t[1] if t[4] == 'income' else -t[1] for t in transactions)
    # Teile Transaktionen in Einnahmen und Ausgaben
    incomes = [t for t in transactions if t[4] == 'income']
    expenses = [t for t in transactions if t[4] == 'expense']
    return render_template('index.html', transactions=transactions, balance=balance, incomes=incomes, expenses=expenses)

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
        print(f"Fehler beim Löschen: {e}")
        return "Fehler beim Löschen", 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)