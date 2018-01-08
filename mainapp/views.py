from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from .models import ProductCategory, Product
from django.contrib import auth
from django.http import Http404, JsonResponse
from django.template import loader
from django.template.context_processors import csrf
from mainapp.forms import MyRegistrationForm, UserChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


links = [
{'href': 'main', 'name': 'главная'},
{'href': 'catalog', 'name': 'каталог'},
{'href': 'contacts', 'name': 'контакты'}
]


def main(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    content = {
    'title': 'главная',
    'links': links,
    'username': username
    }
    return render(request, 'mainapp/index.html', content)


def catalog(request, page=1):
    username = None
    if request.user.is_authenticated():
        username = request.user.username

    products = Product.objects.filter(is_active=True).order_by('price')
    
    paginator = Paginator(products, 3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
    'title': 'каталог',
    'products': products_paginator,
    'links': links,
    'username': username
    }
    return render(request, 'mainapp/catalog.html', content)


def contacts(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    content = {
    'title': 'контакты',
    'links': links,
    'username': username
    }
    return render(request, 'mainapp/contacts.html', content)


def driveclub(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    content = {
    'title': 'driveclub',
    'links': links,
    'username': username
    }
    return render(request, 'mainapp/driveclub.html', content)

def login(request):
    if request.method == 'POST':
        print("POST data =", request.POST)
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        content = {
        'title': 'главная',
        'links': links,
        'errors': True
        }
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'mainapp/index.html', content)
    raise Http404

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def registration(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        content = {'form': form}
        return render(request, 'mainapp/registration.html', content)
    content = {'form': MyRegistrationForm()}
    return render(request, 'mainapp/registration.html', content)

def admin_page(request):
    users = User.objects.all()
    user_form = MyRegistrationForm()
    return render(request, 'mainapp/admin_page.html', {'users': users, 'form': user_form})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect('/admin')

def create_user(request, user_id=None):
    if request.is_ajax():
        if not user_id:
            user_form = MyRegistrationForm(request.POST)
        else:
            user = get_object_or_404(User, id=user_id)
            user_form = UserChangeForm(request.POST or None, instance=user)
        if user_form.is_valid():
            user_form.save()
            users = User.objects.all()
            html = loader.render_to_string('mainapp/inc_users_list.html', {'users': users}, request=request)
            data = {'errors': False, 'html': html}
            return JsonResponse(data)
        else:
            errors = user_form.errors.as_json()
            return JsonResponse({'errors': errors})
    raise Http404

def get_user_form(request, user_id):
    if request.is_ajax():
        user = get_object_or_404(User, id=user_id)
        user_form = MyRegistrationForm(instance=user)
        context = {'form': user_form, 'id': user_id}
        context.update(csrf(request))
        html = loader.render_to_string('mainapp/inc_registration_form.html', context)
        data = {'errors': False, 'html': html}
        return JsonResponse(data)
    raise Http404            




