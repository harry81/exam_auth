


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
```
