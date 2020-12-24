# sample-flask-project

1. Here we have added Dependency Injection framework (similar to [Guice](https://github.com/google/guice) framework),
<br>
   We have also added transaction support. (Actually for simple cases, we need not transaction library because we could have done `database.session.revert()` instead of `transaction.abort()` in our error handler)
   
   
   