from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Product', back_populates='category', cascade='all, delete')

    def __repr__(self):
        return f"<Category {self.name}>"


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100))

    products = db.relationship('Product', back_populates='brand', cascade='all, delete')

    def __repr__(self):
        return f"<Brand {self.name}>"



class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))

    products = db.relationship('Product', back_populates='supplier')
    supplies = db.relationship('Supply', back_populates='supplier')

    def __repr__(self):
        return f"<Supplier {self.name}>"



class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    size = db.Column(db.String(20))
    color = db.Column(db.String(50))
    description = db.Column(db.Text)

    category = db.relationship('Category', back_populates='products')
    brand = db.relationship('Brand', back_populates='products')
    supplier = db.relationship('Supplier', back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product', cascade='all, delete')
    supply_items = db.relationship('SupplyItem', back_populates='product', cascade='all, delete')

    def __repr__(self):
        return f"<Product {self.name} ({self.price}₽)>"



class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(255))

    orders = db.relationship('Order', back_populates='customer')

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name}>"



# class Employee(db.Model):
#     __tablename__ = 'employees'

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     position_id = db.Column(db.Integer, db.ForeignKey('employee_positions.id'), nullable=False)
#     phone = db.Column(db.String(20))
#     email = db.Column(db.String(100), unique=True)
#     orders = db.relationship('Order', back_populates='employee')
#     supplies = db.relationship('Supply', back_populates='employee')
#     employee_position = db.relationship('employee_position', back_populates='employees')

#     def __repr__(self):
#         return f"<Employee {self.first_name} {self.last_name}>"
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="staff")

    position_id = db.Column(db.Integer, db.ForeignKey('employee_positions.id'))

    # relationships
    position = db.relationship('EmployeePosition', back_populates='employees')
    orders = db.relationship('Order', back_populates='employee')
    supplies = db.relationship('Supply', back_populates='employee')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Employee {self.username} ({self.role})>"


class EmployeePosition(db.Model):
    __tablename__ = 'employee_positions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    employees = db.relationship('Employee', back_populates='position')

    def __repr__(self):
        return f"<Position {self.name}>"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'completed', 'cancelled', name='order_status'), default='pending')
    total_amount = db.Column(db.Numeric(10, 2))

    customer = db.relationship('Customer', back_populates='orders')
    employee = db.relationship('Employee', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade='all, delete')

    def __repr__(self):
        return f"<Order #{self.id} - {self.status}>"


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id}>"


class Supply(db.Model):
    __tablename__ = 'supplies'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    supply_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Numeric(10, 2))

    supplier = db.relationship('Supplier', back_populates='supplies')
    employee = db.relationship('Employee', back_populates='supplies')
    items = db.relationship('SupplyItem', back_populates='supply', cascade='all, delete')

    def __repr__(self):
        return f"<Supply #{self.id} - {self.total_cost}₽>"



class SupplyItem(db.Model):
    __tablename__ = 'supply_items'

    id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('supplies.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    supply = db.relationship('Supply', back_populates='items')
    product = db.relationship('Product', back_populates='supply_items')

    def __repr__(self):
        return f"<SupplyItem supply={self.supply_id} product={self.product_id}>"