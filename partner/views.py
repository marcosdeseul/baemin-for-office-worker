from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PartnerForm, MenuForm
from .models import Menu

URL_LOGIN = '/partner/login/'

# Create your views here.
def index(request):
    ctx = {}
    if request.method == "GET":
        partner_form = PartnerForm()
        ctx.update({"form" : partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(request.POST)
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form" : partner_form})

    return render(request, "index.html", ctx)

def login(request):
    ctx = {}

    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_value = request.GET.get("next")
            if next_value:
                return redirect(next_value)
            else:
                return redirect("/partner/")
        else:
            ctx.update({"error" : "사용자가 없습니다."})

    return render(request, "login.html", ctx)

def signup(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(username, email, password)

        user = User.objects.create_user(username, email, password)
        # Article.objects.create(title="", content="")

    ctx = {}
    return render(request, "signup.html", ctx)

def logout(request):
    auth_logout(request)
    return redirect("/partner/")

@login_required(login_url=URL_LOGIN)
def edit_info(request):
    ctx = {}
    # Article.objects.all() # query
    # partner = Partner.objects.get(user=request.user)
    if request.method == "GET":
        partner_form = PartnerForm(instance=request.user.partner)
        ctx.update({"form" : partner_form})
    elif request.method == "POST":
        partner_form = PartnerForm(
            request.POST,
            instance=request.user.partner
        )
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user = request.user
            partner.save()
            return redirect("/partner/")
        else:
            ctx.update({"form" : partner_form})

    return render(request, "edit_info.html", ctx)

@login_required(login_url=URL_LOGIN)
def menu(request):
    ctx = {}
    # if request.user.is_anonymous or request.user.partner is None:
    #     return redirect("/partner/")
    menu_list = Menu.objects.filter(partner = request.user.partner)
    ctx.update({"menu_list": menu_list})

    return render(request, "menu_list.html", ctx)

@login_required(login_url=URL_LOGIN)
def menu_add(request):
    ctx = {}

    if request.method == "GET":
        form = MenuForm()
        ctx.update({ "form": form })
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else:
            ctx.update({ "form": form })

    return render(request, "menu_add.html", ctx)

@login_required(login_url=URL_LOGIN)
def menu_detail(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    ctx = { "menu" : menu }
    return render(request, "menu_detail.html", ctx)

@login_required(login_url=URL_LOGIN)
def menu_edit(request, menu_id):
    ctx = { "replacement" : "수정" }
    menu = Menu.objects.get(id=menu_id)
    if request.method == "GET":
        form = MenuForm(instance=menu)
        ctx.update({ "form": form })
    elif request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else:
            ctx.update({ "form": form })

    return render(request, "menu_add.html", ctx)

@login_required(login_url=URL_LOGIN)
def menu_delete(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    menu.delete()
    return redirect("/partner/menu/")
