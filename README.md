# BudgetUniversityAPI

Use http://35.196.31.92/ before each command! Ex. http://35.196.31.92/api/budget/

GET '/api/budget/'<br/>
Gets all individual budget of each user

POST '/api/budget/'<br/>
BODY:
{
  "total": 300,
  "username": "ro99"
}
<br/>Adds new budget 


GET '/api/budget/<int:budget_id>/'<br/>
Gets the budget from budget_id


POST '/api/budget/<int:budget_id>/<string:category_name>/'
<br/>BODY:
{
  "spent": 300
}
<br/>
Adds money spent to budget id 


DELETE '/api/budget/<int:budget_id>/'
<br/>
Deletes budget id


GET '/api/budget/<int:budget_id>/categories/'
<br/>
Gets all categories from budget id


POST '/api/budget/<int:budget_id>/category/'
<br/>
BODY: 
{
  "name": "Food"
}
<br/>
Adds new category into budget id


POST 'api/budget/<int:budget_id>/<string:category_name>/'
<br/>
BODY:
{
   "name": Chipotle,
   "total": 10
}

Adds item to the category 
<br/>
GET 'api/budget/<int:budget_id>/<string:category_name>/'
<br/>
Gets all the items in that category

