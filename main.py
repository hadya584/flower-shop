import sqlite3, random
from flask import Flask, session, render_template, redirect, url_for, session, flash, request

app = Flask('app')
app.secret_key = "secret"

# Home page to display all products and categories
@app.route('/')
def index():
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  categories = connection.execute('SELECT DISTINCT category FROM products').fetchall()
  products = connection.execute('SELECT * FROM products').fetchall()
  connection.close()
  return render_template('index.html', products=products, categories=categories)

# Displays the products in each category
@app.route('/category/<category>')
def category(category):
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  products = connection.execute('SELECT * FROM products WHERE category = ?', (category,)).fetchall()
  categories = connection.execute('SELECT DISTINCT category FROM products').fetchall()
  connection.close()
  return render_template('category.html', products=products, category=category, categories=categories)

# Searches for products by name
@app.route('/search')
def search():
  query = request.args.get('q', '')
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  products = connection.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + query + '%',)).fetchall()
  categories = connection.execute('SELECT DISTINCT category FROM products').fetchall()
  connection.close()
  return render_template('search.html', products=products, query=query, categories=categories)

# Checks that the username and password matches a user in the database
def check_user(username, password):
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
  connection.close()
  return user 

# Handles user login
@app.route('/login', methods=['GET', 'POST'])
def login():
  # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables! 
  if request.method == 'POST':
    username = request.form.get("username")
    password = request.form.get("password")
    user = check_user(username, password)
    if user:
      session['user'] = username
      session['cart'] = {}
      return redirect(url_for('index'))
    else:
      return render_template('login.html', error="Invalid username or password")
  return render_template('login.html', error=None)
  # Else, give an error message and redirect them to the same login page 

# Handles signup for new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    # Checks if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
      flash('Username already exists.')
    else:
      # Insets new user into the database
      connection.execute('INSERT INTO users (username, password, fname, lname) VALUES (?, ?, ?, ?)', (username, password, fname, lname))
      connection.commit()
      flash('Account created successfully, please log in')
      return redirect(url_for('login'))
    connection.close()
  return render_template('signup.html')

# Adds an item to the shopping cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
  if 'user' not in session:
    flash('Please Login')
    return redirect(url_for('login'))
  quantity = int(request.form['quantity'])
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  # Gets the product by its id
  product = connection.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
  connection.close()
  cart = session.get('cart', {})
  # Adds or updates item quantity in the cart
  cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
  session['cart'] = cart
  flash('Added to cart!')
  return redirect(url_for('index'))

# Displays the shopping cart
@app.route('/cart')
def cart():
  if 'user' not in session:
    flash('Please Login')
    return redirect(url_for('login'))
  cart = session.get('cart', {})
  items = []
  total = 0
  connection = sqlite3.connect('store.db')
  cursor = connection.cursor()
  # Gets the product details for each item in the cart
  for pid, qty in cart.items():
    product = connection.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    if product:
      subtotal = round(product[4] * qty, 2) 
      items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
      total += subtotal
      total = round(total, 2)
  categories = connection.execute('SELECT DISTINCT category FROM products').fetchall()
  connection.close()
  return render_template('cart.html', items=items, total=total, categories=categories)

# Clears all items in the cart
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
  session['cart'] = {}
  flash('Cart has been cleared.')
  return redirect(url_for('cart'))

# Completes the purchase and updates inventory
@app.route('/checkout')
def checkout():
  cart = session.get('cart', {})
  if not cart:
    flash('Cart is empty')
    return redirect(url_for('cart'))
  connection = sqlite3.connect('store.db')
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  total = 0
  # Checks product is available in desired quantity
  for pid, qty in cart.items():
    product = connection.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    if not product or product['quantity'] < qty:
      flash(f'Not enough stock for {product["name"]}.')
      connection.close()
      return redirect(url_for('cart'))
    total += product['price'] * qty
  # Creates a new order
  order_num_str = generate_order_num()
  cursor.execute('INSERT INTO orders (username, total, order_numb) VALUES (?, ?, ?)', (session['user'], total, order_num_str))
  order_num = cursor.execute('SELECT last_insert_rowid()').fetchone()[0]
  # Inserts each item into order_items and updates the stock
  for pid, qty in cart.items():
    product = connection.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    subtotal = product['price'] * qty
    connection.execute('INSERT INTO order_items (order_num, product_id, quantity, subtotal) VALUES (?, ?, ?, ?)', (order_num, pid, qty, subtotal))
    connection.execute('UPDATE products SET quantity = quantity - ? WHERE id = ?', (qty, pid))
  connection.commit()
  connection.close()
  # Clears the cart
  session['cart'] = {}
  flash('Thank you for your order!')
  return redirect(url_for('order_history'))

# Displays the users order history
@app.route('/order_history')
def order_history():
  if 'user' not in session:
    flash('Please Login')
    return redirect(url_for('login'))
  connection = sqlite3.connect('store.db')
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  # Gets all past orders by the user
  orders = connection.execute('SELECT * FROM orders WHERE username = ? ORDER BY date DESC', (session['user'],)).fetchall()
  details = []
  # Gets all items for each order
  for order in orders:
    items = connection.execute('SELECT p.name, oi.quantity, oi.subtotal FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE order_num = ?', (order['id'],)).fetchall()
    details.append({'order': order, 'items': items})
  categories = connection.execute('SELECT DISTINCT category FROM products').fetchall()
  connection.close()
  return render_template('order_history.html', details=details, categories=categories)

def generate_order_num():
  first = 100000000000
  increment = random.randint(1000, 9999)
  last = session.get("last_order_number", first)
  new_order_number = last + increment
  session["last_order_number"] = new_order_number
  return str(new_order_number)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
  # Log the user out and redirect them to the login page
  session.clear()
  return redirect('/')

app.run(host='0.0.0.0', port=8080)