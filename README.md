### 개발환경 구축하기
- 코드 다운로드
```
$ git@github.com:harry81/exam_auth.git
```

- python 가상환경에 필요한 패키지 설치
```
$ pip install -r requirements.txt
```

### 로컬 환경에서 실행하기
```
$ python manage.py runserver

```

### 로그인
- 식별가능 대상
  - username
  - email
  - phone number


### CLI 환경에서 기능 테스트
- 전화번호를 이용해 인증번호 요청하기
```
$ curl -X POST http://localhost:8000/ably/request_verification/ -H 'Content-Type: application/json' -d '{"phone_number": "010-1111-2222"}'

"8448"%
```

- 가입하기
```
$ curl -X POST http://localhost:8000/dj-rest-auth/registration/ -H 'Content-Type: application/json' -d '{"username": "ably1", "password1": "complex_hello", "password2": "complex_hello", "nickname": "공수래공수거", "phone_number": "010-1234-7890", "phone_verified": "8448"}'

{"key":"37ac30f7d75d2141129ef444fdfe819046c1f822"}%
```

- 사용자 정보 조회하기
```
$ url -X GET http://localhost:8000/ably/my/  -H 'Authorization: Token 8777015b268455f7e8c4f9630b010a928634166b' | jq .

{
  "id": 5,
  "username": "ably4",
  "email": "",
  "nickname": "공수래공수거",
  "phone_number": "010-1111-1112"
}

```

- 비밀번호 초기화 하기
전화번호 인증
```
$ curl -X POST http://localhost:8000/ably/request_verification/ -H 'Content-Type: application/json' -d '{"phone_number": "010-1111-1112", "action": "RESET"}'
"5891"%

```

비밀번호 재설정
```
$ curl -X POST http://localhost:8000/dj-rest-auth/registration/reset/ -H 'Content-Type: application/json' -d '{"password1": "complex_hello2", "password2": "complex_hello2","phone_number": "010-1111-1112", "phone_verified": "5891"}'
"OK"%
```
