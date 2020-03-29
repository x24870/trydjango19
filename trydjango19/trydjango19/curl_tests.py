'''
REST Test Examples

Get token:
curl -X POST -d "username=pyk&password=123" http://127.0.0.1:8000/api/auth/token
Returned token:
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InB5ayIsImV4cCI6MTU4NTQ4MTI4MiwiZW1haWwiOiIxMjNAMTIzLmNvbSJ9.UseH7PH3_cTX1_iuI_420LsjZ2IoZyR4A0mysci2tf8

Access API without token
curl http://127.0.0.1:8000/api/comments/

Access API with token
curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InB5ayIsImV4cCI6MTU4NTQ4MTI4MiwiZW1haWwiOiIxMjNAMTIzLmNvbSJ9.UseH7PH3_cTX1_iuI_420LsjZ2IoZyR4A0mysci2tf8" http://127.0.0.1:8000/api/comments/

Create comment with API
curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InB5ayIsImV4cCI6MTU4NTQ4MTI4MiwiZW1haWwiOiIxMjNAMTIzLmNvbSJ9.UseH7PH3_cTX1_iuI_420LsjZ2IoZyR4A0mysci2tf8" -X POST -d "content=Create this comment by API" "http://127.0.0.1:8000/api/comments/create/?type=post&slug=pyk2-created-20"
Create child comment with API to above comment
curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InB5ayIsImV4cCI6MTU4NTQ4MTI4MiwiZW1haWwiOiIxMjNAMTIzLmNvbSJ9.UseH7PH3_cTX1_iuI_420LsjZ2IoZyR4A0mysci2tf8" -X POST -d "content=Child comment of -> Create this comment by API" "http://127.0.0.1:8000/api/comments/create/?type=post&slug=pyk2-created-20&parent_id=26"

'''