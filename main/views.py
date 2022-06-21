from django.shortcuts import render,redirect,get_object_or_404
from .models import Post, Comment
from django.utils import timezone
# mainpage view 함수
def showmain(request):
    posts = Post.objects.all()
    return render(request, 'main/mainpage.html',{'posts':posts})

def posts(request):
    posts = Post.objects.all()
    return render(request, 'main/posts.html', {'posts':posts})

# firstpage view 함수
def showfirst(request):
    return render(request, 'main/firstpage.html')


# secondpage view 함수
def showsecond(request):
    return render(request, 'main/secondpage.html')

def detail(request,id):
    post = get_object_or_404(Post, pk = id )
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'main/detail.html', {'post':post, 'comments':all_comments})

def new(request):
    return render(request,'main/new.html')
def create(request):
    new_post = Post()
    new_post.title = request.POST['title']
    new_post.writer = request.user
    new_post.pub_date = timezone.now()
    new_post.body = request.POST['body']
    new_post.image=request.FILES.get('image')
    new_post.save()
    return redirect('main:detail',new_post.id)

def edit(request,id):
    edit_post= Post.objects.get(id=id)
    return render(request,'main/edit.html',{'post':edit_post})

def update(request,id):
    update_post = Post.objects.get(id=id)
    update_post.title = request.POST['title']
    update_post.writer = request.user
    update_post.image = request.POST['image']
    update_post.pub_date = timezone.now()
    update_post.body = request.POST['body']
    update_post.save()
    return redirect('main:detail', update_post.id)

def delete(request,id):
    delete_post=Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:posts')



def create_comment(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        current_user = request.user
        comment_content = request.POST.get("content")
        Comment.objects.create(content=comment_content, writer=current_user, posts=posts)
    return redirect("main:detail", id)


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        return render(request, "main/edit_comment.html", {"comment": comment})
    else:
        return redirect("main:detail", comment.post.id)

def update_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.content = request.POST.get("content")
    comment.save()
    return redirect("main:detail", comment.post.id)

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        comment.delete()
    return redirect("main:detail", comment.post.id)