# sample-flask-project

Here we have created `autoapp.py` which will serve as entrypoint for Flask app Framework.
<br>
Also, we have created some config classes for Dev and Prod.
For now, we'll use in-memory DB even in prod environment. 
We have `.env` file containing environment variables, we need `python-dotenv` library to use this file.

Next, we have `Dockerfile` containing commands on how to create docker image.
The base image is chosen as per suggestions from this post (https://pythonspeed.com/articles/base-image-python-docker-images/)
<br>You can try different images, if you want.

We have also used flask-migrate framework to support database migration (creating, updating tables in the database).

We have also created a `docker-compose.yml` file to run MySQL image and build our app (you can build docker image of our app using docker build command as well).

Note: Remember to use ` --no-cache` option along with build command when docker starts using cache while running the command (it will inform you on terminal).

You'll also notice the changes in `user_controller.py` file: we have used database now instead of fake data.

Also, there's `static_controller.py` added, this can be used to serve static files from our app, for now it is just for `favicon.ico` which is automatically requested when you open the URL in browser.
The URL for opening the app in the browser will be printed on the terminal when you run the app.
