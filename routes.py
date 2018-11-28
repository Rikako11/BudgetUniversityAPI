import json
from db import db, Budget, Category
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
def get_budget():
    budget = Budget.query.all()
    #Category.query.delete()
    #Budget.query.delete()
    #db.session.commit()
    res = {'success': True, 'data': [budget.serialize() for variables in budget]} 
    return json.dumps(res), 200

@app.route('/api/budget/', methods=['PUT'])
def create_budget():
    budget_body = json.loads(request.data)

    budget = Budget(
		total = buget_body.get('total')
        username = budget_body.get('username')
    )
	
    db.session.add(budget)
    db.session.commit()
    return json.dumps({'success': True, 'data': budget.serialize()}), 201

@app.route('/api/budget/<int:budget_id>/')
def get_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first() 
    if budget is not None:
        return json.dumps({'success': True, 'data': budget.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404
	
@app.route('/api/budget/<int:budget_id>/<int:category_id>', methods=['POST'])
def spend_budget(budget_id):
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is not None:
		category = Category.query.filter_by(budget_id=budget_id, id=category_id).first()
		if category is not None:
			budget_body = json.loads(request.data)
			budget.spent += budget_body.get('spent', budget.spent)
			category.total += budget_body.get('spent', budget.spent)
			if budget.spent <= budget.total:
				db.session.commit()
			else:
				return json.dumps({'success': False, 'error': 'You are spending overbudget!'})
        else:
			return json.dumps({'success': False, 'error': 'Category not found!'}), 404
        return json.dumps({'success': True, 'data': budget.serialize()}), 200
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
        category = Category(
			name = category_body.get('name'),
		    total = 0,
            username = category_body.get('username'),
            budget_id = budget.id
        )
        budget.categories.append(category)
        db.session.add(category)
        db.session.commit()
        return json.dumps({'success': True, 'data': category.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Budget not found!'}), 404 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
