# views.py

def blog_new(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid(): # 이 시점에 모든 유효성 검사가 실행된다. 모든 것이 참이어야만한다.
            form.save()
    else:
        form = BlogForm()


'''
form.is_valid()를 호출한다면

1. form.full_clean() 호출하고
    - 필드별 유효성 검사를 수행하여 필드별 에러를 체크한다
        - 특정필드.clean()을 통해서 Form/Model Field validators 수행
        - form.clean_특정필드()
    - form.clean() 호출하여 다수 필드에 대한 에러를 체크한다.
2. 에러가 있었다면 Flase를 리턴하고 없으면 True를 리턴한다.



즉 
1. validator 함수를 통한 유효성 검사와
    - 값이 원하는 조건에 맞지 않을때 예외 발생시키고 리턴값 쓰지 않는다.
2. Form 클래스 내에 clean 멤버함수를 통한 유횽성 검사 및 값을 변경한다.
    - 값이 원하는 조건에 맞지 않을때 에러 발생시키고 리턴 값을 통해 값을 변환한다.
    
모든 validators는 모델에 정의해라 # 어드민에서도 쓸 수 있고 모델폼에서도 쓸수있고 알아보기도 쉽다.
ModelForm을 통해 모델의 validators 정보도 같이 가져와라

clean은 언제 쓰나?

1. 특정 form에서 1회성 유효성 검사 루틴이 필요할 때 # validator는 재사용성
2. 다수 필드 값을 묶어서 유효성 검사가 필요할 때
3. 필드 값을 변경할 필요가 있을 때 validator를 통해서는 값을 변경할 수가 없다. 단지 값의 조건만 체크할 뿐이다
'''
# 2번의 예 여러가지 서버에서 이름을 검사할 때

# models.py
class GameUser(models.Model):
    server = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    
# forms.py
class GameUserSignupForm(forms.ModelForm):
    class Meta:
        model = GameUser
        field = ['server', 'username']

    def clean_username(self):
        # 'username 필드 값의 좌/우 공백을 제거하고 최소 3글자 이상 입력되었는지 체크'
        username = self.cleaned_data.get('username','').strip()
        if username:
            if len(username) < 3:
                raise forms.ValidationError('3글자 이상 입력해주세요')
            # 이 리턴 값으로 self.cleaned_data['username'] 값이 변경됩니다.
            # 좌우 공백이 제거된 (strip) username으로 변경됩니다.
            return username

    def clean(self):
        cleaned_data = super().clean()
        if self.check_exist(cleaned_data['server'], cleaned_data['username']):
            raise forms.ValidationError('서버에 이미 등록된 username입니다')
        return cleaned_data

    def check_exist(self, server, username):
        return GameUser.objects.filter(server=server, username=username).exists()


# 간결하게 모델에 있는 기능을 적용해서 사용하고자 할 경우

from django.core.validators import MinLengthValidator

class GameUser(models.Model):
    server = models.CharField(max_length=10)
    username = models.CharField(max_length=20, validators = [MinLengthValidator(3)])

    class Meta:
        unique_together = [
            ('server', 'username'),
        ]

class GameUserSignupForm(forms.ModelForm):
    class Meta:
        model = GameUser
        fields = ['server', 'username']

    def clean_username(self):
        '값 변환은 clean 함수에서만 가능합니다. validator에서는 지원하지 않습니다.'
        return self.cleaned_data.get('username', '').strip()

#admin

admin.site.register(GameUser)




# 예시

class CommentForm(forms.Form):
    def clean_message(self):
        return self.cleaned_data.get('message', '').strip() # 좌우공백이 제거되었다.
        
# 뷰단 

form = CommentForm(request.POST)
if form.is_valid():
    
    message = request.POST['message']  # 좌우공백이 제거되지 않은 데이터를 가져오게된다.
    comment = Comment(message=message)
    comment.save()
    return redirect(post)

form = CommentForm(request.POST)
if form.is_valid():
    
    message = form.cleaned_data['message'] # 좌우공백이 제거된 데이터를 가져온다.
    comment = Comment(message=message)
    comment.save()
    return redirect(post)
    
    
# 함수 validator는 snake_case, 클래스  validator는 CamelCase
# 클래스 validator의 인스턴스는 함수처럼 호출가능하다. __call__


'''
validator의 인자 지원

1. 모델 필드 정의시

def test_validator(value):
    pass
    
# models.py
# 모델 폼에서 적용 뿐만 아니라 모델 자체에서 벨리데이터를 적용시켜서 한번에 적용시킬 수 있다.
class Post(models.Model):
    title = models.CharField(validators = [test_validator]
    
2. 폼 필드에서 정의시

폼 필드에서는 폼에서 validtaor를 적용시켜 줘야한다.
'''


'''
장고는 1프로젝트 멀티앱 각 앱별로 쓰이는 정적인 파일은 따로따로 넣어주는 것이 좋다. 공통적으로 쓰면 공통의 부분에 넣어주는 것이 좋을 것이다. 
# static files

- 개발 리소스 로서의 정적인 파일(js, css, image, etc)
    - 앱단위로 저장/서빙
    - 프로젝트 단위로 저장/서빙
    
- Media Files : 유저가 업로드한 모든 정적인 파일(image, etc)
    -프로젝트 단위로 저장/서빙


settings

1.
# 정적인 파일을 요청할 경우, 뷰함수 요청의 경우 함수인지 파일인지 구분해야한다. 그 구분점이 /static/이다. 
STATIC_URL = '/static/'

2.
# 전체를 모으고자 할때 어느 부분에 모을 것인가를 지정해주는 부분, 1개면 충분하다
STATICFILES_DIRS = [
    os.path.join(BASE_DIR(최상위 프로젝트 루트), 'trydjango'(프로젝트명), 'static'(프로젝트 경로)),
]

3.
# 개발 시가 아니라 배포시에는 모든 앱에 있떤 스태틱 파일 디렉토리들을 모아야한다. 개발당시에는 의미가 없다.
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')



## static files finder

'''