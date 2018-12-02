# BudgetUniversityAPI

Use http://35.196.31.92/ before each command! Ex. http://35.196.31.92/api/budget/

GET '/api/budget/'  
Gets all individual budget of each user  
RESPONSE:  
[{  
"id": 1,
"total": 200,
"spent": 0,
"username": ro99
}]

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


POST 'api/budget/<int:budget_id>/<string:category_name>/'  
BODY:
{
   "name": Chipotle,
   "total": 10
}  
Adds item to the category 

GET 'api/budget/<int:budget_id>/<string:category_name>/'  
Gets all the items in that category

