# megaportal_crk

curl -X POST 'http://127.0.0.1:8080/user/signup' -H "accept: application/json" -H "Content-Type: application/json" -d '{"username": "fastapi", "password": "Stro0ng!"}'


curl -X POST 'http://127.0.0.1:8080/user/signin' \
-H 'accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=password&username=fastapi&password=Stro0ng!&scope=&client_id=&client_secret='

curl -X GET "http://127.0.0.1:8080/request/" -H "accept: application/json"
curl -X GET "http://127.0.0.1:8080/request/" -H "accept: application/json" -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZmFzdGFwaSIsImV4cGlyZXMiOjE3MzUyMDA1NjUuMjc3OTIzfQ.3rbU-c5WskJugRAsX53vzErGHpmH-K7pUS1Ulyh4h_Y'