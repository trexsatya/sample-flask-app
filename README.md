# sample-flask-project

1. Create `app/controllers` package, and `user_controller.py` to contain controller code
2. Move `create_app` method from `conftest.py` to `app/main.py`
3. Make sure that you have `__init__.py` in tests folder and app folder.
   (This becomes a bit tricky if you were developing a python library. See here: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure)
   <br> But we are creating an application, so it seems fine.
4. Run `pytest`, your tests should pass, which means we have a functioning REST API for users.
5. `jsonify` is a useful helper method, see its documentation. You could simply return (data, response_code) from the controller