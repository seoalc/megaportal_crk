# megaportal_crk

curl -X POST 'http://127.0.0.1:8080/user/signup' -H "accept: application/json" -H "Content-Type: application/json" -d '{"username": "fastapi", "password": "Stro0ng!"}'


curl -X POST 'http://127.0.0.1:8080/user/signin' \
-H 'accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=password&username=fastapi&password=Stro0ng!&scope=&client_id=&client_secret='