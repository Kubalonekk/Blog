from django.shortcuts import render
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.db.models.fields.files import ImageFieldFile, FileField
from .filters import *
from django.db.models import Q


def index(request):

    posts = Post.objects.filter(published=True).order_by('-creation_date')[:3]
    print(datetime.now())
    context = {
        'posts': posts,

    }

    return render(request, 'Blog/index.html', context)


def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        NewUserProfile = UserProfile.objects.create(
            user=new_user,
            name=first_name,
            last_name=last_name,
            email=email,
        )
        authenticated_user = authenticate(
            username=new_user.username,
            password=request.POST['password1'])
        login(request, authenticated_user)
        messages.success(request, 'Pomyślnie założno konto')
        return HttpResponseRedirect(reverse('index'))

    context = {
        'form': form,
    }

    return render(request, 'Blog/register.html', context)


def signout(request):
    logout(request)
    messages.success(request, 'Pomyślnie wylogowano')
    return redirect('index')


@user_passes_test(lambda u: u.groups.filter(name='Content creators').exists())
def CreatePost(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES.getlist('images')
        new_post = Post.objects.create(
            userprofile=request.user.userprofile,
            title=data['title'],
            text=data['text'],
            published=data['published'],
        )
        ImagePost.objects.create(
            post=new_post,
            image=request.FILES.get('main_image'),
            main_image=True
        )

        for f in files:
            new_image = ImagePost.objects.create(
                post=new_post,
                image=f
            )
        messages.success(request, 'Pomyślnie dodano post')
        return redirect('single_post', pk=new_post.id)

    context = {}

    return render(request, 'Blog/create_post.html', context)


def delete_comment(request, pk):
    comment = PostComment.objects.get(id=pk)
    if request.user.userprofile == comment.user:     
        comment.delete()
        messages.success(request, 'Pomyślnie usunięto komentarz')
    else:
        messages.warning(request, 'Nie mozesz dostepu')
    return redirect('single_post', comment.post.id)


def single_post(request, pk):
    post = Post.objects.get(id=pk)
    post_images = ImagePost.objects.filter(post=post, main_image=False)
    comments = PostComment.objects.filter(post=post).order_by('-creation_date')
    post.viewCount += 1
    post.save()
    if request.method == "POST":
        if request.user.is_authenticated:
            post_comment  = request.POST.get('post_comment')
            new_comment = PostComment.objects.create(
                user = request.user.userprofile,
                post = post,
                text = post_comment,
            )
            messages.success(request, 'Dodałeś nowy komentarz')
            return redirect('single_post', pk=post.id)
        else:
            messages.warning(request, 'Tylko zalogowani użytkownicy mają możliwość komentowania')
            return redirect('login')
            
    else:
        pass
        

    context = {
        'post': post,
        'comments': comments,
        'post_images': post_images,
    }

    return render(request, 'Blog/single_post.html', context)


def search_results(request):

    if request.method == 'POST':
        searched = request.POST.get('searched')
        post_list = Post.objects.filter(
            title__icontains=searched, published=True).order_by('-creation_date')
    else:
        post_list = Post.objects.all()
    context = {
        'post_list': post_list,
    }

    return render(request, 'Blog/search_results.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@user_passes_test(lambda u: u.groups.filter(Q(name='Content creators',) | Q(name='Moderators',) ).exists())
def dashboard(request):

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        title = request.POST.get('title')
        published = request.POST.get('published')
        if published == "empty":
            if start and end is None:
                posts = Post.objects.filter(title__icontains=title)
            else:  
                posts = Post.objects.filter(creation_date__gte=start, creation_date__lte=end,title__icontains=title, )
        else:
            posts = Post.objects.filter(creation_date__gte=start, creation_date__lte=end, title__icontains=title, published=published)

    else:
        posts = Post.objects.all().order_by("-creation_date")

    context = {
            'posts': posts,
        }
    

    return render(request, 'Blog/dashboard.html', context)

@user_passes_test(lambda u: u.groups.filter(Q(name='Content creators',) | Q(name='Moderators',) ).exists())
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    messages.success(request, 'Pomyślnie usunięto post')
    return redirect('dashboard')

@user_passes_test(lambda u: u.groups.filter(Q(name='Content creators',) | Q(name='Moderators',) ).exists())
def edit_post(request, pk):
    post = Post.objects.get(id=pk)

    form = CreatePostForm(instance=post)

    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('edit_post_images', pk=post.id)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'Blog/edit_post.html', context)

@user_passes_test(lambda u: u.groups.filter(Q(name='Content creators',) | Q(name='Moderators',) ).exists())
def edit_post_images(request, pk):
    post = Post.objects.get(id=pk)
    post_images = ImagePost.objects.filter(post=post).order_by('-main_image')
    main_post_image = ImagePost.objects.get(post=post, main_image=True)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES.getlist('images')
        image = request.FILES.get('main_image')
        if image != None:
            new_image = ImagePost.objects.create(
                post=post,
                image=image,
                main_image=True
            )
            for q in post_images:
                if q != new_image and q.main_image == True:
                    q.main_image = False
                    q.save()
        else:
            pass

        for f in files:
            new_image = ImagePost.objects.create(
                post=post,
                image=f
            )

    context = {
        'post': post,
        'post_images': post_images,
        'main_post_image': main_post_image,
    }

    return render(request, 'Blog/edit_post_images.html', context)




@user_passes_test(lambda u: u.groups.filter(Q(name='Content creators',) | Q(name='Moderators',) ).exists())
def delete_post_image(request, pk):
    image = ImagePost.objects.get(id=pk)
    image.delete()
    messages.success(request, 'Pomyślnie usunięto zdjęcie')
    return redirect('edit_post_images', image.post.id)


def custom_page_not_found_view(request, exception):
    return render(request, "Blog/404.html", {})





