import json
from db import db, Budget, Category, Item
from flask import Flask, request

db_filename = "todo.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/api/budget/')
def get_budgets():
    budgets = Budget.query.all()
    res = {'success': True, 'data': [budget.serialize() for budget in budgets]} 
    return json.dumps(res), 200

@app.route('/api/budget/', methods=['DELETE'])
def delete_all():
    Category.drop_all()
    db.session.commit()
    return json.dumps({'success':True})

@app.route('/api/budget/', methods=['POST'])
def create_budget():
    budget_body = json.loads(request.data)
    budget = Budget.query.filter_by(username=budget_body.get('username')).first()
    if budget is None: 
        budget = Budget(
	   total = budget_body.get('total'),
           spent = 0,
           username = budget_body.get('username')
        )
        db.session.add(budget)
    else:
       budget.total = budget_body.get('total') 
    db.session.commit()
    return json.dumps({'success': True, 'data': budget.serialize()}), 201

@app.route('/api/budget/<int:budget_id>/')
def get_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first() 
    if budget is not None:
        return json.dumps({'success': True, 'data': budget.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/<string:category_name>/', methods=['POST'])
def spend_budget(budget_id, category_name):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        category = Category.query.filter_by(budget_id=budget_id, name=category_name).first()
        if category is not None:
            budget_body = json.loads(request.data)
            spent = budget_body.get('spent', budget.spent)
            item = Item(
                name = budget_body.get('name'),
                total = spent,
                category_id = category.id,
                budget_id = budget.id
            )
            budget.spent += spent
            category.total += spent
            if budget.spent <= budget.total:
                category.items.append(item)
                db.session.add(item)
                db.session.commit()
                return json.dumps({'success': True, 'data': item.serialize()}), 200
            return json.dumps({'success': False, 'error': 'You are spending overbudget!'})
        return json.dumps({'success': False, 'error': 'Category not found!'}), 404
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/<string:category_name>/')
def get_items(budget_id, category_name):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        category = Category.query.filter_by(id=budget_id, name=category_name).first()
        if category is not None:
            items = [item.serialize() for item in category.items]
            return json.dumps({'success': True, 'data': items}), 200
        return json.dumps({'success': False, 'error': 'Category not found!'}), 404
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/', methods=['DELETE'])
def delete_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first() 
    if budget is not None:
        db.session.delete(budget)
        db.session.commit()
        return json.dumps({'success': True, 'data': budget.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404 

@app.route('/api/budget/<int:budget_id>/categories/')
def get_categories(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        categories = [category.serialize() for category in budget.categories]
        return json.dumps({'success': True, 'data': categories}), 200
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/category/', methods=['POST'])
def create_category(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        category_body = json.loads(request.data)
        category_name = category_body.get('name')
        category = Category.query.filter_by(budget_id=budget_id, name=category_name).first()
        if category is None:
            category = Category(
                name = category_name,
                total = 0,
                budget_id = budget.id
            )
            budget.categories.append(category)
            db.session.add(category)
            db.session.commit()
            return json.dumps({'success': True, 'data': category.serialize()}), 201
        return json.dumps({'success': False, 'error': 'Category already exists!'}), 201
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/<string:category_name>/<int:item_id>/', methods=['DELETE'])
def delete_it(budget_id, category_name, item_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        category = Category.query.filter_by(budget_id=budget_id, name=category_name).first()
        if category is not None:
            item = Item.query.filter_by(id=item_id, budget_id=budget_id, category_name=category_name).first()
            if item is not None:
                budget.spent -= item.total
                category.total -= item.total
                db.session.delete(item)
                db.session.commit()
                return json.dumps({'success': True, 'data': budget.serialize()}), 200
            return json.dumps({'success': False, 'error': 'Item not found!'}), 404
        return json.dumps({'success': False, 'error': 'Category not found!'}), 404
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

@app.route('/api/budget/<int:budget_id>/<string:category_name>/', methods=['DELETE'])
def delete_category(budget_id, category_name):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
        category = Category.query.filter_by(budget_id=budget_id, name=category_name).first()
        if category is not None:
            budget.spent -= category.total
            db.session.delete(category)
            db.session.commit()
            return json.dumps({'success': True, 'data': budget.serialize()}), 200
        return json.dumps({'success': False, 'error': 'Category not found!'}), 404
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
