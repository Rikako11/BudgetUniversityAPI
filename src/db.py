from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    spent = db.Column(db.Integer)
    username = db.Column(db.String, nullable=False)
    categories = db.relationship('Category', cascade='delete')

    def __init__(self, **kwargs):
        self.total = kwargs.get('total','')
        self.spent = kwargs.get('spent','')
        self.username = kwargs.get('username', '')

    def serialize(self):
        return {
            'id': self.id,
            'total': self.total,
            'spent': self.spent,
            'username': self.username
        }

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    total = db.Column(db.Integer)
    items = db.relationship('Item', cascade='delete')
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.total = kwargs.get('total','')
        self.budget_id = kwargs.get('budget_id')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'total': self.total
        }

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    total = db.Column(db.Integer)
    category_name = db.Column(db.Integer, db.ForeignKey('category.name'), nullable=False) 
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.total = kwargs.get('total', '')
        self.category_name = kwargs.get('category_name')
        self.budget_id = kwargs.get('budget_id')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'total': self.total,
        }
