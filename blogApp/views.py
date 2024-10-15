from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json, datetime
from django.contrib.auth.models import User
from django.contrib import messages
from blogApp.models import UserProfile,Category,Section,Folder,Post,PageHindi,PageBengali,PageMarathi,PageTamil
from django.shortcuts import render, redirect, get_object_or_404
from blogApp.forms import UserRegistration, UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, SaveCategory, AddAvatar

category_list = Category.objects.exclude(status = 2).all()
context = {
    'page_title' : 'Simple Blog Site',
}

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def posts(request,sid):
    context['page_title'] = 'Posts'
    posts = Post.objects.all()
    context['posts'] = posts
    context['page'] = 'posts'

    return render(request, 'posts.html',context)

@login_required
def sections(request):
    context['page_title'] = 'Sections'
    sections = Section.objects.all()
    context['sections'] = sections
    context['page'] = 'sections'
    return render(request,'sections.html',context)

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            newUser = User.objects.all().last()
            try:
                profile = UserProfile.objects.get(user = newUser)
            except:
                profile = None
            if profile is None:
                UserProfile(user = newUser, dob= data['dob'], contact= data['contact'], address= data['address'], avatar = request.FILES['avatar']).save()
            else:
                UserProfile.objects.filter(id = profile.id).update(user = newUser, dob= data['dob'], contact= data['contact'], address= data['address'])
                avatar = AddAvatar(request.POST,request.FILES, instance = profile)
                if avatar.is_valid():
                    avatar.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request,'register.html',context)

@login_required
def profile(request):
    context = {
        'page_title':"My Profile"
    }

    return render(request,'profile.html',context)
    
@login_required
def update_profile(request):
    context['page_title'] = "Update Profile"
    user = User.objects.get(id= request.user.id)
    profile = UserProfile.objects.get(user= user)
    context['userData'] = user
    context['userProfile'] = profile
    if request.method == 'POST':
        data = request.POST
        # if data['password1'] == '':
        # data['password1'] = '123'
        form = UpdateProfile(data, instance=user)
        if form.is_valid():
            form.save()
            form2 = UpdateProfileMeta(data, instance=profile)
            if form2.is_valid():
                form2.save()
                messages.success(request,"Your Profile has been updated successfully")
                return redirect("profile")
            else:
                # form = UpdateProfile(instance=user)
                context['form2'] = form2
        else:
            context['form1'] = form
            form = UpdateProfile(instance=request.user)
    return render(request,'update_profile.html',context)


@login_required
def update_avatar(request):
    context['page_title'] = "Update Avatar"
    user = User.objects.get(id= request.user.id)
    context['userData'] = user
    context['userProfile'] = user.profile
    img = user.profile.avatar.url

    context['img'] = img
    if request.method == 'POST':
        form = UpdateProfileAvatar(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Profile has been updated successfully")
            return redirect("profile")
        else:
            context['form'] = form
            form = UpdateProfileAvatar(instance=user)
    return render(request,'update_avatar.html',context)

#Category
@login_required
def category_mgt(request):
    categories = Category.objects.all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'category_mgt.html',context)

@login_required
def manage_category(request,pk=None):
    # category = Category.objects.all()
    if pk == None:
        category = {}
    elif pk > 0:
        category = Category.objects.filter(id=pk).first()
    else:
        category = {}
    context['page_title'] = "Manage Category"
    context['category'] = category

    return render(request, 'manage_category.html',context)

@login_required
def save_category(request):
    resp = { 'status':'failed' , 'msg' : '' }
    if request.method == 'POST':
        category = None
        if not request.POST['id'] == '':
            category = Category.objects.filter(id=request.POST['id']).first()
        if not category == None:
            form = SaveCategory(request.POST,instance = category)
        else:
            form = SaveCategory(request.POST)
    if form.is_valid():
        form.save()
        resp['status'] = 'success'
        messages.success(request, 'Category has been saved successfully')
    else:
        for field in form:
            for error in field.errors:
                resp['msg'] += str(error + '<br>')
        if not category == None:
            form = SaveCategory(instance = category)
       
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def delete_category(request):
    resp={'status' : 'failed', 'msg':''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            category = Category.objects.filter(id = id).first()
            category.delete()
            resp['status'] = 'success'
            messages.success(request,'Category has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp),content_type="application/json")

#Post
@login_required
def post_mgt(request):
    if request.user.profile.user_type == 1:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(author = request.user).all()

    context['page_title'] = "post Management"
    context['posts'] = posts
    return render(request, 'post_mgt.html',context)


from googletrans import Translator
LANGUAGE_MODEL_MAP = {
        'Hindi': PageHindi,
        'Bengali': PageBengali,
        'Tamil': PageTamil,
        'Marathi': PageMarathi,
        'English':Post,
    }

def get_folder_breadcrumbs(folder):
    breadcrumbs = []
    current_folder = folder    
    while current_folder:
        breadcrumbs.insert(0, current_folder)
        current_folder = current_folder.parent_folder
    return breadcrumbs

from bs4 import BeautifulSoup
from googletrans import Translator

def translate_text(html_content, language):
    lang_code = {
        'Hindi': 'hi',
        'Bengali': 'bn',
        'Tamil': 'ta',
        'Marathi': 'mr',
        'English': 'en',
    }
    src = lang_code['English']
    dest = lang_code[language]
    translator = Translator()    
    soup = BeautifulSoup(html_content, 'html.parser')
    for text_node in soup.find_all(string=True):
        if text_node.strip():
            translated_text = translator.translate(text_node, src=src, dest=dest).text
            text_node.replace_with(translated_text)
    return str(soup)


def create_translated_page(post, language):
    model = LANGUAGE_MODEL_MAP[language]
    translated_title = translate_text(post.title, language)
    translated_blog_post = translate_text(post.blog_post, language)
    banner = post.banner
    translated_page = model.objects.create(
        post=post,
        title=translated_title,
        blog_post=translated_blog_post,
        banner=banner
    )
    return translated_page

##########################################################################################################################################
def create_folder(request, section_id, parent_folder_id=None):
    section = get_object_or_404(Section, id=section_id)
    parent_folder = None
    if parent_folder_id:
        parent_folder = get_object_or_404(Folder, id=parent_folder_id)
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        Folder.objects.create(section=section, name=folder_name, parent_folder=parent_folder)
        if parent_folder:
            return redirect('folder_view', folder_id=parent_folder.id)
        else:
            return redirect('section_view', section_id=section.id)
    return render(request, 'create_folder.html', {
        'section': section,
        'parent_folder': parent_folder
        })

def create_post(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        page_name = request.POST.get('page_name')
        page_title = request.POST.get('page_title')
        side_panel = request.POST.get('side_panel')
        map_image = request.POST.get('map_image')
        body_content = request.POST.get('body_content')
        static_table = request.POST.get('static_table')
        dynamic_table = request.POST.get('dynamic_table')
        new_post = Post.objects.create(
            folder=folder,
            page_name=page_name,
            page_title=page_title,
            side_panel=side_panel,
            map_image=map_image,
            body_content=body_content,
            static_table=static_table,
            dynamic_table=dynamic_table
        )
        i=0
        print(request.POST)
        while f'map_name_{i}' in request.POST:
            map_name = request.POST.get(f'map_name_{i}')
            map_thumbnail_name = request.POST.get(f'map_thumbnail_{i}')
            map_alt = request.POST.get(f'map_alt_{i}')
            print(map_name)
            print(map_thumbnail_name)
            print(map_alt)
            i+=1
        return redirect('edit-post', lang='English', pk=new_post.id)
    return render(request, 'create_post.html', {
        'folder': folder,
        'breadcrumbs':get_folder_breadcrumbs(folder)+[{'name':'Create page'}]
        })


def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)    
    subfolders = folder.subfolders.all()
    posts = folder.posts.all()
    return render(request, 'folder_view.html', {
        'folder': folder,
        'subfolders': subfolders,
        'posts': posts,
        'page': 'folder_view',
        'breadcrumbs': get_folder_breadcrumbs(folder)
    })

def section_view(request, section_id):
    section = get_object_or_404(Section, id=section_id)    
    root_folders = Folder.objects.filter(section=section, parent_folder__isnull=True)
    return render(request, 'section_view.html', {
        'section': section,
        'root_folders': root_folders,
        'page':'section_view'
    })

########################################################################################################################################################
@login_required
def edit_post(request,lang,pk,tr=None):
    post = Post.objects.get(id=pk)
    folder = post.folder
    if lang != 'English':
        model = LANGUAGE_MODEL_MAP[lang]
        try:
            en_post = Post.objects.get(id=pk)
            post = model.objects.get(post=en_post)
            print(post.blog_post)
            if tr:
                post.title = translate_text(en_post.title,lang)
                post.blog_post = translate_text(en_post.blog_post,lang)
                post.save()
        except model.DoesNotExist:
            post = create_translated_page(post, lang)
    context = {
        'page_title': "Edit post",
        'post': post,
        'pk':pk,
        'selected_language': lang,
        'folder':folder,
        'breadcrumbs':get_folder_breadcrumbs(folder)+[{'name':post.page_name}]
    }
    return render(request, 'edit_post.html', context)


@login_required
def edit_section(request,pk):
    section = Section.objects.get(id=pk)
    context = {
        'page_title': "Edit Section",
        'section': section,
        'pk':pk,
    }
    return render(request, 'edit_section.html', context)

@login_required
def edit_folder(request,pk):
    folder = Folder.objects.get(id=pk)
    if request.method == 'POST':
        folder.name = request.POST['folder_name']
        folder.save()
        if folder.parent_folder:
            return redirect('folder_view', folder_id=folder.parent_folder.id)
        else:
            return redirect('section_view', section_id=folder.section.id)
    return render(request,'edit_folder.html',{'folder':folder})

@login_required
def delete_folder(request,pk):
    folder = Folder.objects.get(id=pk)
    folder.delete()
    if folder.parent_folder:
        return redirect('folder_view', folder_id=folder.parent_folder.id)
    else:
        return redirect('section_view', section_id=folder.section.id)




@login_required
def add_post(request):
    context = {
        'page_title': "Add post",
    }
    return render(request, 'add_post.html', context)

@login_required
def add_section(request):
    context = {
        'page_title': "Add Section",
    }
    return render(request, 'add_section.html', context)


@login_required
def save_post(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if 'id' in request.POST:
            post = Post.objects.get(id=request.POST['id'])
            if request.POST['lang'] != 'English':
                model = LANGUAGE_MODEL_MAP[request.POST['lang']]
                post = model.objects.get(post=post)
            
            post.page_name = request.POST['page_name']
            post.page_title = request.POST['page_title']
            post.side_panel = request.POST['side_panel']
            post.map_image = request.POST['map_image']
            post.body_content = request.POST['body_content']
            post.static_table = request.POST['static_table']
            post.dynamic_table = request.POST['dynamic_table']

            
            post.save()
            resp['status'] = 'success'
            messages.success(request, 'Post has been saved successfully')
        else:
            post = Post.objects.create(
                title=request.POST['title'],
                blog_post=request.POST['blog_post'],
                banner=request.FILES['banner']
            )
            resp['status'] = 'success'
            resp['pk'] = post.id
            messages.success(request, 'Post has been saved successfully')
        
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def save_section(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if 'id' in request.POST:
            section = Section.objects.get(id=request.POST['id'])
            section.title = request.POST['title']
            if 'theme' in request.FILES:
                section.theme = request.FILES['theme']
            section.save()
            resp['status'] = 'success'
            messages.success(request, 'Section has been created successfully')
        else:
            section = Section.objects.create(
                title=request.POST['title'],
                theme=request.FILES['theme']
            )
            resp['status'] = 'success'
            messages.success(request, 'Section has been created successfully')
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_post(request,pk):
    resp={'status' : 'failed', 'msg':''}
    try:
        post = Post.objects.filter(id = pk).first()
        folder_id = post.folder.id
        post.delete()
        resp['status'] = 'success'
        messages.success(request,'Post has been deleted successfully.')
    except Exception as e:
        raise print(e)
    return redirect('folder_view',folder_id)

@login_required
def delete_section(request,pk):
    resp={'status' : 'failed', 'msg':''}
    try:
        section = Section.objects.filter(id = pk).first()
        section.delete()
        resp['status'] = 'success'
        messages.success(request,'Section has been deleted successfully.')
    except Exception as e:
        raise print(e)
    return redirect('sections-page')


def view_post(request,pk=None):
    context['page_title'] = ""
    if pk is None:
        messages.error(request,"Unabale to view Post")
        return redirect('home-page')
    else:
        post = Post.objects.filter(id = pk).first()
        context['page_title'] = post.title
        context['post'] = post
    return render(request, 'view_post.html',context)

def post_by_category(request,pk=None):
    if pk is None:
        messages.error(request,"Unabale to view Post")
        return redirect('home-page')
    else:
        category = Category.objects.filter(id=pk).first()
        context['page_title'] = category.name
        context['category'] = category
        posts = Post.objects.filter(category = category).all()
        context['posts'] = posts
    return render(request, 'by_categories.html',context)

def categories(request):
    categories = Category.objects.filter(status = 1).all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'categories.html',context)