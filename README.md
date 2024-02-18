To run this project

1. First activate the virtual env (venv)
     command -> MacOS source bin/activate
2. Then run server inside the notes directory
     command -> python3 manage.py runserver
3. To invoke any API other than /login and /signup we need csrf token
   1. To get csrf token first make account using /singup
           payload -> {
                             "username": "anupprakash",
                             "email": "anup@gmail.com",
                             "password": "123"
                         }
   2. Then /login
      payload -> {
                   "username": "anup_prakash",
                   "password": "123"
               }
      in the response we will get csrf token

4. To use csrf token in the header
    key -> X-CSRFToken
   value -> <csrf_token>
