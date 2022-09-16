### 개발환경 구축하기
- 코드 다운로드
```
$ git clone git@github.com:harry81/exam_auth.git
```

- python 가상환경에 필요한 패키지 설치
```
$ pip install -r requirements.txt
```

### 사용한 web framework

[Django](https://djangopackages.org)


### 로컬 환경에서 실행하기
```
$ python manage.py runserver
```
http://localhost:8000/admin/ 에서 저장된 데이타를 확인할 수 있습니다. 또는 데모용으로 운용중인 https://ably.hoodpub.com/ 에서도 확인 가능합니다.

<img src="https://hm-public-static.s3.ap-northeast-2.amazonaws.com/images/sc-ably-admin.png" width="700px">

### 배포환경

 - AWS Lambda + API Gateway(https://github.com/zappa/Zappa#about)
 - PostgreSQL 13.7 on AWS

<img src="https://hm-public-static.s3.ap-northeast-2.amazonaws.com/images/sc-ably-admin-on-aws.png" width="700px">

### Endpoints
```
$ python manage.py show_urls

/ably/my/       ably.views.MyGetView
/ably/request_verification/     ably.views.RequestVerificationView
/dj-rest-auth/login/    dj_rest_auth.views.LoginView    rest_login
/dj-rest-auth/registration/reset/       ably.views.ResetPasswordView
```

### 로그인
- 식별가능 대상
  - username
  - email
  - phone number


### CLI 환경에서 기능 테스트 하기
- 전화번호 인증요청하기 하면 네 자리의 숫자를 반환합니다. 1분 이내에 이 숫자와 함께 `가입하기`, `비밀번호 초기화하기` 를 요청한 경우에만 유효하다고 판단, 즉 실제 sms를 전송하지 않고 인증에 성공하였다고 간주하였습니다.

<img src="https://hm-public-static.s3.ap-northeast-2.amazonaws.com/images/sc-ably-list-verification.png" width="700px">


#### 전화번호로 인증번호 요청하기

성공하면 네자리의 `인증키`를 반환합니다.
```
$ curl -X POST http://localhost:8000/ably/request_verification/ -H 'Content-Type: application/json' -d '{"phone_number": "010-1111-1118"}'

"2513"
```

#### 가입하기(registration)

성공하면 token `key` 를 반환합니다.
```
$ curl -X POST http://localhost:8000/dj-rest-auth/registration/ -H 'Content-Type: application/json' -d '{"username": "ably8", "password1": "complex_hello", "password2": "complex_hello", "nickname": "공수래공수거5", "phone_number": "010-1111-1118", "email": "user8@a-bly.com", "phone_verified": "2513"}'

{"key":"77be8f038c2d590ec30568b65d40d3c32b5fb8e8"}
```

#### 사용자 정보 조회하기
```
$ url -X GET http://localhost:8000/ably/my/  -H 'Authorization: Token 77be8f038c2d590ec30568b65d40d3c32b5fb8e8 | jq .

{
  "id": 9,
  "username": "ably8",
  "email": "user8@a-bly.com",
  "nickname": "공수래공수거5",
  "phone_number": "010-1111-1118"
}
```

#### 비밀번호 초기화하기

- 전화번호 인증
```
$ curl -X POST http://localhost:8000/ably/request_verification/ -H 'Content-Type: application/json' -d '{"phone_number": "010-1111-1112", "action": "RESET"}'
"5891"%
```

- 비밀번호 재설정
```
$ curl -X POST http://localhost:8000/dj-rest-auth/registration/reset/ -H 'Content-Type: application/json' -d '{"password1": "complex_hello2", "password2": "complex_hello2","phone_number": "010-1111-1112", "phone_verified": "5891"}'
"OK"%
```



### 소감
 - 퀴즈형 코딩 테스트가 아니어서 흥미롭게 과제를 진행할 수 있었습니다.
 - Django 에서 제공하는 기본적인 Auth를 이용했습니다. 기본 기능 외에 Customizing 을 해야하는 경우는 처음이라 새로운 개념(serializer, adapter)를 알 수 있었습니다.
 - TDD를 적용해서 작업했습니다. 덕분에 목표지향적으로 코딩할 수 있었습니다.


### Test Cases
```
class AuthTestCase(TestCase):
    def setUp(self):
    def test_request_verification(self):
    def test_register(self):
    def test_register_with_invalid_key(self):
    def test_login_with_username(self):
    def test_login_with_phone_number(self):
    def test_login_with_email(self):
    def test_login_with_email(self):
    def test_reset_password(self):
```
