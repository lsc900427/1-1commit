# OAuth란

'''
open id로 개발된 표준 인증방식
각 서비스 별로 다 다른 인증방식을 하나로 표준화
인증을 공유하는 어플리케이션끼리는 라이브러리 하나로 인증 가능
'''

# 라이브러리 종류

'''
django-oauth-toolkit
python-social-auth
django-allauth
'''

# 로그인 방법

'''
# settings.py

- settings/INSTALLED_APPS에 제공 코드를 추가하고 admin페이지를 통해
  클라이언트키/서버키 등록

- settings에 django.contrib.sites 필요(이 서비스를 기본 전제로 만들어짐)

- SITE_ID = 1 추가 필수
  등록하지 않으면 host명의 Site 인스턴스를 찾음
  
- SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
  없으면 메일 인증을 하게 함, none이어야 즉시 로그인 가능
'''

# views.py
'''
def login(request):
    providers = []
    for provider in get_providers():
        
        try:
            #소셜 앱별로 키 등록 여부 확인
            provider.social_app = SocialApp.objects.get(
                                                provider=provider.id,
                                                sites=settings.SITE_ID)
        except SocailApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)
    
        
    return auth_login(request,
        authentication_form = LoginForm,
        template_name='ac/login.html',
        extra_context={'providers': providers})
        # 넘겨주고 추가 인자를 넘겨준다.
'''

# login_form.html

'''
{{ providers }}를 통해 값을 불러옴
'''


#보여지는.html

'''
<img src="{{ user.socialaccount_set.all.first.get_avatar_url }}">(프로필 상의 주소를 가져온다)

user와 socialaccount는 1:N 관계이기 떄문에 _set.all 메서드를 사용했다.

'''

#이제 웹에서
'''
이제 웹에서 필요한 클라이언트키와 시크릿키를 받는 과정을 통해 적용시키면 끝
'''

# brief
'''
실제로 프로젝트 진행한 내용을 추가해가면서 내용을 더 추가하자.ㅇㅇ
'''
