[33mcommit 11b9bc460f14f3bf23cf3be81ab6adb9b3c5f357[m[33m ([m[1;36mHEAD -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 19:38:59 2020 +0900

    1. requirements.txt : sqlparse version downgraded
    2. accountApp/models.Customer의 누락된 user_image field 복구

[33mcommit 733ee263a778c7fd730ac199fbd2afe275171ba0[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 19:32:57 2020 +0900

    requirements.txt 복구: 종속성 해결

[33mcommit ddf8b6561d90bda7a6b6381c82faa3b8bf95095a[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 19:28:29 2020 +0900

    requirements.txt 복구

[33mcommit 2f48117a9d0004692b39e84ee42bb8999dfa8bba[m
Author: hkh0105 <깃허브 이메일! hkh9601@naver.com>
Date:   Sat Nov 14 19:22:21 2020 +0900

    update

[33mcommit bb1085524292aa4991c5126f0d93c6114f10a901[m
Merge: 2d184bd d503fe4
Author: hkh0105 <깃허브 이메일! hkh9601@naver.com>
Date:   Sat Nov 14 19:05:15 2020 +0900

    Merge branch 'master' of https://github.com/pcjs156/Match_Tattoo

[33mcommit 2d184bdfd4a6f6cebd23b5e98278e4eb7a3f50dc[m
Author: hkh0105 <깃허브 이메일! hkh9601@naver.com>
Date:   Sat Nov 14 19:05:07 2020 +0900

    중간저장

[33mcommit d503fe4feac56649d5a9b5304166703ec99ddc6a[m
Merge: b490b2e c89f428
Author: hkh0105 <62933450+hkh0105@users.noreply.github.com>
Date:   Sat Nov 14 18:36:02 2020 +0900

    Merge pull request #2 from pcjs156/matchingApp_basis
    
    Matching app basis

[33mcommit c89f428987d05db903efd8f71f6e5e537f55125e[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 02:54:52 2020 +0900

    delete_matching 구현

[33mcommit a5445ea86c0092b1f35097f6292e3874f22e5e87[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 02:50:44 2020 +0900

    modify_matching 구현

[33mcommit 4d0e36c277ff19778afb60fdd528c3600829c7cb[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 02:14:20 2020 +0900

    detail_matching 구현

[33mcommit f95c3bfa96d6cc6749b424257b1264845eb5624b[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sat Nov 14 01:43:56 2020 +0900

    Matching 모델 create 구현
    1. matchingApp/models/Matching model에 title(제목) field 추가
    2. matchingApp/views/create_matching_view 구현 (forms.py 추가)
    3. 만약 tattooist만 접근 가능한 view에 접근 권한이 없는 유저가 접근할 때 이동될 customer_request_rejected Template, view 추가

[33mcommit 7c462c9f01e5f13a2b680ab93751a59fe6f3c282[m
Merge: 1c218cb b490b2e
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Thu Nov 12 21:12:38 2020 +0900

    Merge branch 'master' of https://github.com/pcjs156/Match_Tatoo into matchingApp_basis

[33mcommit b490b2e617ab90bf1af3b6559ca92f4b5dd38a32[m
Merge: ae5a8b5 9e887da
Author: Yu-bin Park <itqkrdbqls1001@naver.com>
Date:   Thu Nov 12 21:10:07 2020 +0900

    Merge pull request #1 from pcjs156/accountApp_basis
    
    Account app basis

[33mcommit 1c218cba1835b191045d128eb8b0264306573fe2[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 11 23:31:57 2020 +0900

    matching_list 페이지 구현
    1. tools.py
      - parse_dict_from_code_pair
      - reversed_dict
    
    2. matchingApp/models.py
     - 길이가 너무 긴 행의 중간에서 개행함
     - 지역/유형/부위 정보가 코드로 저장되므로, 이를 페이지에서 원래 값으로 보여주기 위한 get_(region/tattoo_type/part) 메서드 추가
    
    3. matchingApp/views/matching_list_view 구현
     - GET 방식으로 region, type, part, order-by 값을 가져와 Matching의 조건 검색과 정렬에 사용
     - 조건 변경과 정렬방식 변경은 추후 구현 예정
    
    4. mainApp/templates/intro.html
     - 연결된 링크의 조건에 맞는 Matching 목록을 GET 방식으로 matching_list_view에 전달
    
    5. matchingApp/templates/matching_list.html
     -  bulma css의 table component class를 적용, 조건에 맞는 데이터가 있는 경우와 없는 경우를 템플릿 문법으로 제어
    
    +) bulma CDN version updated (9.0 -> 0.1) (in templates/base.html)
    +) Migration file 추가

[33mcommit 9e887da4e9eb5ca54ee6cebbc3850f485860b99d[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 11 01:20:41 2020 +0900

    collectstatic

[33mcommit a0956ab7a1fa07f7bba7260c94e91f26d23b692a[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 11 01:20:32 2020 +0900

    회원가입 기능 구현
    1. select_user_type.html : 유저 타입을 결정하는 페이지
    2. signup_customer/tattooist: 회원가입 페이지
         - signup.css: signup_customer/tattooist에 공통적으로 적용될 css
         - 각 뷰는 정보(username, pw, email, nickname의 유효성을 검사함(tools.User/TattoolstChecker)
            : 유효성 정보를 담은 객체를 template에 전달해 입력 정보가 유효하지 않을 때 적절한 에러 메시지가 뜨도록 구현
    
    +) base.html 개선: 메인/회원가입 redirect link 추가

[33mcommit 54dbbb13aa5659e1e0cdd2806a5f79ee67e642a5[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Tue Nov 10 23:41:14 2020 +0900

    1. 로그인 / 로그아웃 기능 구현 + url 연결
    2. base.html nav 태그에 로그인/비로그인 사용자마다 다르게 계정 정보?가 뜨도록 구현
        - 로그인한 사용자: username [ nickname(없을 경우 에러메시지) ] / 로그아웃
        - 로그인하지 않은 사용자: 로그인

[33mcommit 140c3ac0a4a7c4d9094d5897df1e831d6420a501[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Tue Nov 10 23:22:07 2020 +0900

    1. already_logged_in.html/css 파일 이름 수정
    2. 이미 로그인한 사용자가 접근할 수 없는 페이지에 접근을 시도할 경우 already_logged_in 페이지로 이동하도록 코드 추가

[33mcommit ae09c5735c4103bc2e501fd855ea0199ebd17a02[m
Merge: e75c2f0 ae5a8b5
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Tue Nov 10 22:42:43 2020 +0900

    Merge branch 'master' of https://github.com/pcjs156/Match_Tatoo into accountApp_basis

[33mcommit ae5a8b5723ec26779095c3c01fd18429133d3124[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Tue Nov 10 22:41:22 2020 +0900

    누락된 date_upload_to 추가

[33mcommit e75c2f0e90ef157e1c43a40e7fd0fdb865345900[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Tue Nov 10 22:37:46 2020 +0900

    이미 로그인된 유저가 이동될 "already_logged_in" 페이지 생성 + CSS/url/view 연결

[33mcommit 80fcb2e16221b5d988c8fc01541eb4732599f97a[m
Author: Jooyoung <pyoungjy@gmail.com>
Date:   Mon Nov 9 20:03:09 2020 +0900

    date_upload_to 수정 및 추가
    
    1. tools.py 수정
    2. accountApp models.py의 Customer class에 date_upload_to 적용
    3. tattooistApp models.py의 Portfolio class, Review class에 date_upload_to 적용

[33mcommit cab6c9c702fdb273b196f80de2525f245bfa9bf9[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Sun Nov 8 20:44:30 2020 +0900

    1. requirements.txt 수정: Django downgrade
    2. accountApp/mainApp/matchingApp/tattooistApp 모델 설계 완료
    3. match_tattoo/settings.py AUTH_USER_MODEL 추가
    4. 앱별 admin 추가
    5. tools.date_upload_to 추가

[33mcommit 71862f04ae09cc6400440702112b4138b3857d0b[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 03:43:46 2020 +0900

    matchingtApp template/CSS 생성 / url 연결

[33mcommit 11eae578c720d4b3df25952c8ede84e7ec387ae7[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 03:30:09 2020 +0900

    accountApp template/CSS 생성 / url 연결

[33mcommit cd79db7c3139dd811bcc7ff5290f9a279ffb2db0[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 03:16:57 2020 +0900

    tattooistApp template/CSS 생성 / url 연결

[33mcommit 295bd1e4b8c7bbb185b8a2ad0a5c882cddf06ebe[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 03:16:23 2020 +0900

    mainApp view에 주석 추가

[33mcommit 97c8c340ae52b8ead0520abf22ecfdf7e410efe1[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 02:43:41 2020 +0900

    mainApp template/CSS 생성 / url 연결

[33mcommit 905f3e79019f0bd447ecf3d1d3ec77dc2d2f0405[m
Author: yubin <itqkrdbqls1001@naver.com>
Date:   Wed Nov 4 02:07:35 2020 +0900

    1. 프로젝트 생성
    2. 앱 생성
    3. 관련 디렉토리, 필수 파일 생성
    4. app별 url include
    5. 최초 migration
    6. gitignore 생성
    7. requirements.txt 생성
