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


LOGIN
![Screenshot 2024-02-19 at 12 21 32 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/3db371eb-d8b8-4bce-87f5-fe9f8268bef3)


SIGN-UP
![Screenshot 2024-02-19 at 12 22 14 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/bc1d23c5-cc92-4752-a8b7-60c21f83eb9c)


LOGUT
![Screenshot 2024-02-19 at 12 23 15 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/99e4984f-95cd-4268-b512-260744a52aeb)

GET SPECIFI NOTE
![Screenshot 2024-02-19 at 12 23 47 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/519391fd-0b9f-4c85-ab30-81b22d663e7c)

UPDATE NOTE
![Screenshot 2024-02-19 at 12 24 20 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/e62b5535-046f-4748-bde2-c15f47dd8f39)


SHARE NOTES
![Screenshot 2024-02-19 at 12 24 36 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/3353c618-d378-4807-88fa-08eaab070151)


NOTES VERSION
![Screenshot 2024-02-19 at 12 24 58 AM](https://github.com/nerds-coding/Django-Notes/assets/45892153/d4691692-b5f0-48c1-829d-758e6990feae)















