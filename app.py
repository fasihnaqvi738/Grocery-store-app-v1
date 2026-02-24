import os 
from flask import Flask , render_template , request , redirect , session ,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash

current_dir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"  + os.path.join(current_dir, "database.db")

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key='secret-key'



class customers(db.Model):
    __tablename__ = 'customers'
    pid = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50))
    contact = db.Column(db.Integer, unique = True, nullable = False)
    email = db.Column(db.String(20), unique = True)
    address = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



class categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement= True, nullable = False)
    category_name = db.Column(db.String(20))
    products = db.relationship('product', backref='categories', lazy=True)



class product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key = True, unique=True, autoincrement=True)
    product_name = db.Column(db.String(50), nullable = False)
    unit = db.Column(db.String(50), nullable = False)
    rate_per_unit = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id') , nullable = False)



class cart(db.Model):
    __tablename__ = 'cart'
  
    cart_product_id = db.Column(db.Integer, db.ForeignKey('product.product_id') , nullable = False ,primary_key = True)
    pid = db.Column(db.Integer, db.ForeignKey('customers.pid'), nullable = False , primary_key = True)
    product_quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer)
    



@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         contact = request.form['contact']
#         email = request.form['email']
#         address = request.form['address']
#         username = request.form['username']
#         password = request.form['password']
#         user = customers(name=name, contact=contact, email=email, address= address, username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        
        existing_user = customers.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken! Please choose a different username', 'error')
            return redirect(url_for('register'))
        
        existing_user = customers.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already taken! Please choose a different email', 'error')
            return redirect(url_for('register'))
        
        existing_user = customers.query.filter_by(contact=contact).first()
        if existing_user:
            flash('Contact no. already taken! Please choose a different contact no', 'error')
            return redirect(url_for('register'))
        
        user = customers(name=name, contact=contact, email=email, address=address, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect(url_for('index'))

    return render_template('register.html')



# @app.route('/login', methods= ['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         data = customers.query.filter_by( username=username, password=password ).first()

#         if data:
#             session['name']=data.name
#             session['password']=data.password
#             pid = data.pid
#             return redirect(url_for('user_dashboard' , pid=pid))
        
#     return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = customers.query.filter_by(username=username, password=password).first()

        if data:
            session['name'] = data.name
            session['password'] = data.password
            pid = data.pid
            return redirect(url_for('user_dashboard', pid=pid))
        else:
            flash('Invalid username or password entered!', 'error')
            
    return redirect(url_for('index'))




@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/admin_login_page')
def admin_login_page():
    return render_template('admin_login_page.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



@app.route('/admin_login',methods=['GET', 'POST'])
def admin_login():
    if request.method=='POST':
        admin_username=request.form['username']
        admin_password=request.form['password']
        if admin_username=='admin123' and admin_password=='adminpass':
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login_page.html')
    else:
        return render_template('admin_login.html')



@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    category_list = categories.query.all()
    products = product.query.all()
    return render_template('admin_dashboard.html' , categories = category_list , product = products)


@app.route('/user_dashboard/<int:pid>',methods = ['GET', 'POST'])
def user_dashboard(pid):
    customer = customers.query.get(pid)
    category_list = categories.query.all()
    products = product.query.all()
    pid = customers.query.get(pid)
    return render_template('user_dashboard.html' , categories = category_list , product = products , customer = customer , pid=pid)



@app.route('/add_category',methods= ['GET','POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category = categories(category_name=category_name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('add_category.html')




@app.route('/delete_category', methods=['POST'])
def delete_category():
   
    category_id = request.form.get('category_id')
    category = categories.query.get(category_id)
    if category:
        products_to_be_deleted = product.query.filter_by(category_id = category_id).all()
        for prod in products_to_be_deleted:
            db.session.delete(prod)


        db.session.delete(category)
        db.session.commit()
        

    return redirect(url_for('admin_dashboard'))



@app.route('/add_product/<int:category_id>', methods=['GET', 'POST'])
def add_product(category_id):
   
    category = categories.query.filter_by(category_id = category_id).first()

    if request.method == 'POST':
        # cid = request.args.get('category_id')
        product_name = request.form.get('product_name')
        unit = request.form.get('unit')
        rate_per_unit = request.form.get('rate')
        quantity = request.form.get('quantity')



        new_product = product(product_name=product_name, unit=unit, rate_per_unit=rate_per_unit, quantity=quantity , category_id = category_id)

        db.session.add(new_product)
        db.session.commit()

    
        return redirect(url_for('admin_dashboard'))

    return render_template('add_product.html' , category = category)



@app.route('/product_actions/<int:product_id>',methods = ['GET', 'POST'])
def product_actions(product_id):
    
    return render_template('product_actions.html'  , product_id = product_id)



@app.route('/delete_product', methods=['POST'])
def delete_product():
   
    product_id = request.args.get('product_id')
    product_for_deletion = product.query.get(product_id)
    if product_for_deletion:
       

        db.session.delete(product_for_deletion)
        db.session.commit()
        
    return redirect(url_for('admin_dashboard'))




@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product_to_edit = product.query.get(product_id)
    
    if request.method == 'POST':
        old_quantity = product_to_edit.quantity  # Store the old quantity before updating
        product_to_edit.product_name = request.form.get('product_name')
        product_to_edit.unit = request.form.get('unit')
        product_to_edit.rate_per_unit = request.form.get('rate')
        product_to_edit.quantity = request.form.get('quantity')

        db.session.commit()

        # Reduce the product quantity in the cart if it has changed
        if old_quantity != product_to_edit.quantity:
            cart_items = cart.query.filter_by(cart_product_id=product_id).all()
            for cart_item in cart_items:
                if cart_item.product_quantity > product_to_edit.quantity:
                    cart_item.product_quantity = product_to_edit.quantity
                    cart_item.total_amount = product_to_edit.rate_per_unit * product_to_edit.quantity
            db.session.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('edit_product.html', product=product_to_edit, product_id=product_id)




@app.route('/edit_category/<int:category_id>', methods = ['GET' , 'POST'])
def edit_category(category_id):
    category_to_edit = categories.query.get(category_id)

    if request.method == 'POST':
        category_to_edit.category_name = request.form.get('category_name')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_category.html' , category_id = category_id ,category_to_edit = category_to_edit)



@app.route('/summary')
def summary():
    return render_template('summary.html')




@app.route('/cart/<int:pid>', methods=['GET', 'POST'])
def user_cart(pid):
    grand_total = 0
    customer = customers.query.get(pid)
    
    cart_items = db.session.query(cart, product).join(product, (product.product_id == cart.cart_product_id) & (cart.pid == pid)).all()
    cart_products = []

    for product_item in cart_items:
        cart_products.append(product_item)
    
    for item in cart_items:
        if item.product.quantity > 0:
            grand_total += item.cart.total_amount
    return render_template('cart.html', customer=customer, cart_products=cart_products , pid = pid , grand_total = grand_total)





@app.route('/user_profile/<int:pid>' , methods=['GET'])
def user_profile(pid):
    customer = customers.query.get(pid)
    return render_template('user_profile.html' , customer = customer ,pid = pid)




@app.route('/add_to_cart', methods=['GET' , 'POST'])
def add_to_cart():
    
    if request.method == 'GET':
        pid = request.args.get('pid')
        product_id = request.args.get('cart_product_id')
        product_quantity = request.args.get('product_quantity')
       
        cart_item = cart.query.filter_by(cart_product_id=product_id, pid=pid).first()
        if cart_item:
            current_product = product.query.get(product_id)

            if cart_item.product_quantity < current_product.quantity :
                cart_item.product_quantity += 1
                cart_item.total_amount = current_product.rate_per_unit * cart_item.product_quantity
                db.session.commit()
        
        
        
        else:
            cart_item = cart(cart_product_id=product_id, product_quantity=product_quantity, pid=pid , total_amount = 0)
            current_product = product.query.get(product_id)
            cart_item.total_amount = int(current_product.rate_per_unit) * int(cart_item.product_quantity)
            db.session.add(cart_item)
        db.session.commit()

        return redirect(url_for('user_dashboard', pid=pid ))



@app.route('/search/<int:pid>', methods=['GET', 'POST'])
def search(pid):

    customer = customers.query.get(pid)
    if request.method == 'POST':
        
        search_term = request.form.get('search_term')
        products = product.query.all()
        searched_categories = categories.query.filter(categories.category_name.like('%'+search_term+'%')).all()
        searched_products = product.query.filter(product.product_name.like('%'+search_term+'%')).all()

        if searched_products:
            print('found')
        else:
            print('not found')
        
        return render_template('search_result.html', searched_categories=searched_categories, searched_products=searched_products ,pid = pid , customer = customer , product = products)
    else:
        return 'not found'
   





@app.route('/increase_quantity/<int:pid>/<int:product_id>')
def increase_quantity(pid, product_id):
    cart_item = cart.query.filter_by(pid=pid, cart_product_id=product_id).first()
    
    if cart_item:
        current_product = product.query.get(product_id)
        if cart_item.product_quantity < current_product.quantity :
            cart_item.product_quantity += 1
            cart_item.total_amount = current_product.rate_per_unit * cart_item.product_quantity
            db.session.commit()

    return redirect(url_for('user_cart', pid=pid, product_id=product_id))






@app.route('/decrease_quantity/<int:pid>/<int:product_id>')
def decrease_quantity(pid, product_id):
    cart_item = cart.query.filter_by(pid=pid, cart_product_id=product_id).first()
    
    if cart_item:
        if cart_item.product_quantity > 1:
            cart_item.product_quantity -= 1
            current_product = product.query.get(product_id)
            cart_item.total_amount = current_product.rate_per_unit * cart_item.product_quantity
            db.session.commit()
        else:
            db.session.delete(cart_item)  # Delete the cart item directly
            db.session.commit()
    
    return redirect(url_for('user_cart', pid=pid, product_id=product_id))




@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
def remove_from_cart(product_id):
    pid = request.args.get('pid')  # Assuming a specific pid value, modify this based on your requirements

    # Get the cart item based on the product_id and pid
    cart_item = cart.query.filter_by(cart_product_id=product_id, pid=pid).first()

    if cart_item:
        # Remove the cart item from the database
        db.session.delete(cart_item)
        db.session.commit()

    # Redirect to the cart page
    return redirect(url_for('user_cart' , pid=pid))



@app.route('/order_confirmation/<int:pid>')
def order_confirmation(pid):
    customer = customers.query.get(pid)
    return render_template('order_confirmation.html' , customer = customer , pid=pid)



@app.route('/place_order/<int:pid>', methods=['GET'])
def place_order(pid):
    
    cart_items = cart.query.filter_by(pid=pid).all()
    
    

    for cart_item in cart_items:
        cart_product = product.query.get(cart_item.cart_product_id)

        cart_product_id = cart_item.cart_product_id
        

        if cart_product and cart_product.quantity >= cart_item.product_quantity:    
            cart_product.quantity -= cart_item.product_quantity

            others_cart_items = cart.query.filter_by(cart_product_id = cart_product_id).all()

            for other_cart_item in others_cart_items:
                other_cart_item.product_quantity -= cart_item.product_quantity


            db.session.delete(cart_item)

            

    db.session.commit()
    
    return redirect(url_for('order_confirmation' , pid = pid))







if __name__ == '__main__':
    app.run(debug=True)










