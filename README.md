# BudgetUniversityAPI
GET '/api/budget/'
Gets all individual budget of each user

POST '/api/budget/'
BODY:
{
  "total": 300,
  "username": "ro99"
}
Adds new budget 

GET '/api/budget/<int:budget_id>/'
Gets the budget from budget_id

POST '/api/budget/<int:budget_id>/<string:category_name>/'
BODY:
{
  "spent": 300
}
Adds money spent to budget id 

DELETE '/api/budget/<int:budget_id>/'
Deletes budget id

GET '/api/budget/<int:budget_id>/categories/'
Gets all categories from budget id

POST '/api/budget/<int:budget_id>/category/'
BODY: 
{
  "name": "Food"
}
Adds new category into budget id
