# CBV? FBV

'''
파이썬 장고에서는 view라는 것이 존재한다.
view란 결국 호출가능한 객체다.
rquest가 오면 url에 접근하고
url에서 각 뷰 함수를 호출해준다.
view는 CBV와 FBV로 나누어서 생각을 하는데
한글로 풀어쓰면 CBV는 클래스 기반뷰, FBV는 함수 기반뷰이다.
CBV는 as_view라는 클래스 함수를 통해서 함수 뷰를 생성하는데
as_view를 통해서 결국 FBV를 만들어낸다.
CBV는 재사용성이 높고 일반적으로 많이 쓰이는 기능을 쉽게 사용할 수 있도록 함축 시켜놓았다.
FBV와 CBV를 잘 섞어쓰고 어떨 때 둘 중 무엇을 선택할 것인지 빠른 판단을 하는게
실력이 좋은 사람인 듯하다.(물론 둘다 구현가능해야 하겠지만...)
'''



def blog_detail(request, id):

    Blog = get_object_or_404(Post, id = id) # 여기서 id는 db(id), url(id) 같다.

    return render(request, 'blog/blog_detail.html', {
        'Blog': Blog
    }) # 블로그 디테일 템플릿으로 Blog 디테일 페이지를 내려준다.



def generate_view_fn(model):
    def view_fn(request, id):
        instance = get_object_or_404(model, id=id)
        instance_name = model._meta.model_name
        template_name = '{}/{}.blog.html'.format(
            model._meta.app_label, instance_name
        )
        return render(request, template_name, {
            instance_name: instance,
        })
    return view_fn # 이런식으로 감싸서 내부함수를 리턴하는 패턴이 굉장히 많고 이것이 CBV 기본구성 같다.

blog_detail = generate_view_fn(Blog)


def DetailView(object):
    def __init__(self, model):
        self.model = model

    def get_object(self, *args, **kwargs):

        return get_object_or_404(self.model, id = kwargs['id'])

    def get_template_name(self):
        return '{}/{}.detail.html'.format(
            self.model._meta.app_label,
            self.model._meta.model_name,
        )
    def dispatch(self, request, *args, **kwargs):
        return render(request, self.get_template_name(), {
            self.model._meta.model_name: self.get_object(*args,**kwargs),
        })

    @classmethod # cls는 파이썬에서 넘겨오고 model은 내가 넘긴 모델이다.
    def as_view(cls, model):
        def view(request, *args, **kwargs):
            self = cls(model)
            return self.dispatch(request, *args, **kwargs)
        return view

blog_detail = DetailView.as_view(Blog)

# 결국 as_view를 사용했을 때 as_view란 함수가 호출되고 호출될때마다 새로운 view가 생성이된다.



# ListView

'''
보통 Get요청
목적은 지정 모델에 대한 전체 목록을 조회하는 것이다.
'''

blog_list = ListView.as_view(model=Blog, paginate_by = 5)
## url.py
urlpatterns = [
    url(r'^blog/$', views.blog_list),
]


# DetailView

'''
보통 Get요청
지정 pk 또는 slug의 모델 인스턴스의 Detail 페이지를 보여준다.
url에서 pk를 안쓰고 싶을 때 사용 메서드
-> pk_url_kwarg = '내가원하는거'
'''

urlpatterns = [
    url(r'^blog/(?P<pk>\d+)/$', views.blog_detail),
]

# CreateView/UpdateView
'''
GET/POST 요청 ->모델 폼을 통해서 모델 인스턴스를 생성하고 수정한다.

- model옵션이 필수
- form_class : 없으면 모델폼 생성이 된다
- field : form_class 없으면 지정 필드에 대해서 form처리
- success_url : 제공하지 않으면 model_instance.get_absolute_url() 호출시도
- GET요청 : 입력 폼을 보여주고 입력이 완료되면 같은 URL로 POST요청
- POST요청 : 입력받은 POST데이터에 대해 유효성 검사를 수행
    부적합 판정시 다시 입력 폼을 보여주고
    적합 판정시 데이터를 저장하고 , success_url로 이동한다
'''

class BlogForm(forms.ModelFrom):
    class Meta:
        model = BlogFormfields = '__all__'
# 어차피 자동생성되기 때문에 쓰고 안쓰고는 자기선택이다


class BlogCreateView(CreavteView):
    model = Blog
    form_class = BlogForm

blog_new = BlogCreateView.as_view()

blog_edit = BlogUpdateView.as_view(model=Blog, fields='__all__')

blog_delete = BlogDeleteView.as_view(model = Blog, successs_url = '/blog/')