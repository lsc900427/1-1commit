form = CommentForm(request.POST)

if form.is_valid():

    message = request.POST['message']
    comment = Comment(message=message)
    comment.save()
    return redirect(post)

form = CommentForm(request.POST)
if form.is_valid():

    message = form.cleaned_data['message']
    comment = Comment(message=message)
    comment.save()
    return redirect(post)

# 폼은  validation을 통해서 값이 변화할 수 있다. 그렇기에 값을 변화 하기전 raw데이터인
#request.POST['값']을 쓰는 것은 맞지 않다. form.cleaned_data['값']으로 올바르게 사용하자. 즉 끝까지 쓰자는 말이다.

# 모델 폼을 쓰면 모델에 관련해서는 간결하게 폼을 사용할 수 있다.

#html
<a href="{% url "blog:post_edit" post.id %}">글 수정</a>

#urls.py

urlpatterns = [
    url(r'new/$', views.post_new, name = 'post_new')
    url(r'^(?P<id>\d+)/edit/$', view.post_edit, name = 'post_edit')
]

# forms.py

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        field = '__all__'



# views.py

def post_new(request):
    if request.method == 'POST':
        form = PostForm(reqeust.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect(post)

    else:
         form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form,
    })

def post_edit(request):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(reqeust.POST, request.FILES, instance = post)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect(post)

    else:
        form = PostForm(instance = post)

    return render(request, 'blog/post_form.html', {
        'form': form,
    })





