from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_transaction, get_transactions, delete_transaction

app = Flask(__name__)

@app.route('/')
def index():
    transactions = get_transactions()
    balance = sum(t[1] if t[4] == 'income' else -t[1] for t in transactions)
    incomes = [t for t in transactions if t[4] == 'income']
    expenses = [t for t in transactions if t[4] == 'expense']
    print(f"Alle Transaktionen: {transactions}")
    print(f"Einnahmen: {incomes}")
    print(f"Ausgaben: {expenses}")

    # Kategorienübersicht für Ausgaben
    category_summary = {}
    for t in expenses:
        category = t[2]
        category_summary[category] = category_summary.get(category, 0) + t[1]
    print(f"Kategorienübersicht: {category_summary}")  # Debug-Ausgabe
    return render_template('index.html', transactions=transactions, balance=balance, incomes=incomes, expenses=expenses, category_summary=category_summary)

@app.route('/category_overview')
def category_overview():
    transactions = get_transactions()
    expenses = [t for t in transactions if t[4] == 'expense']
    category_summary = {}
    for t in expenses:
        category = t[2]
        category_summary[category] = category_summary.get(category, 0) + t[1]
    return render_template('category_overview.html', category_summary=category_summary)

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
    app.run(host='127.0.0.1', port=5000, debug=False)