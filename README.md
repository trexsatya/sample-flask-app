# sample-flask-project

Here we have used `Flask-HTTPAuth` library to implement JWT token based authentication system.
The authentication is customized social login (only google supported as of now), which works like this:-
1. You get access token from google (This can be easily done by integrating google on UI side)
2. The access token can be sent to our app to register, or login to the application.

Our app verifies the token and then creates its own token to return to the user upon login.

-------

UserController tests have been accordingly modified to pass authentication header.
<br>
There are few small changes in `user` table as well. Remember that after you make any changes in the table/entity models, 
you have to run `flask db migrate` and `flask db upgrade` commands to apply the changes to the database.

--------
Here're some useful commands for manual testing:-<br>
Get the idToken from google. and run `export G_TOKEN=<paste_token_value_here>`
1. curl -X POST -d "{ \"idToken\": \"$G_TOKEN\" , \"social\": \"google\" }" http://127.0.0.1:5000/api/v1/auth/login -H "Content-Type: application/json"
2. curl -H "Authorization: Bearer $token" http://127.0.0.1:5000/api/v1/users

