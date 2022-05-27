from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .forms import AddProductForm
from .models import Product
from .forms import ChatInputForm
from .forms import AddToCartForm
from .forms import CreateChatForm
from .forms import ChatOutputForm

import sqlite3 as sq


class Database_Сonstruction:
    """"
        constructs databases
    """
    @staticmethod
    def creating_tables(db):
        try:
            db.execute("CREATE TABLE products(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " label TEXT,"
                       " likes INTEGER,"
                       " id_category TEXT,"
                       " price INTEGER, "
                       " username TEXT, "
                       " url_img TEXT)")
            db.execute("CREATE TABLE users_products(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " id_product INTEGER,"
                       " id_user INTEGER)")
            db.execute("CREATE TABLE categories(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "name TEXT)")
            db.execute("CREATE TABLE likes(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " id_user INTEGER,"
                       " id_category INTEGER,"
                       " amount INTEGER)")
        except:
            print("Таблицы уже созданы!")


def get_base_context(request, receiver):
    """
        sets base context of context
    """
    menu = [
        {"link": "/chat_list/", "text": "Чаты"},
        {"link": "/shopping_cart/", "text": "Корзина"},
        {"link": "/new_product/", "text": "Добавить товар"},
    ]
    db = sq.connect("db.sqlite3")
    Database_Сonstruction.creating_tables(db)
    products = (db.execute("SELECT * FROM products")).fetchall()

    if str(request.user) != "AnonymousUser":
        username = str(request.user)
        try:
            id_username = (db.execute("SELECT id FROM auth_user WHERE username = " + username).fetchall())[0][0]
        except:
            id_username = "Error"
        if id_username != "Error":
            chat = db.execute("SELECT * FROM chat WHERE id_receiver = " + id_username).fetchall()
            messages = []
            for i in len(chat):
                mes = db.execute("SELECT * FROM messages WHERE id_chat = " + chat[i][0]).fetchall()
                messages.append(mes)
            if receiver != "Anonuser":
                tr_data = db.execute("SELECT id FROM chat WHERE receiver = ?", (username,)).fetchall()
                tr_data2 = db.execute("SELECT sender FROM chat WHERE receiver = ?", (username,)).fetchall()
                for i in range(len(tr_data)):
                    id_chat = tr_data[i]
                messages = db.execute("SELECT * FROM messages WHERE id_chat = ?", id_chat).fetchall()
                return {"messages": messages}
        else:
            chat = {("No login in base")}
    else:
        chat = {("Login to have chats")}
    db.close()
    return {"menu": menu, "user": request.user, "products": products, "chat": chat}


def create_chat(request):
    """"
        func of creating chat
        gets request
        returns render of html-page
    """
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        username = str(request.user)
        with db:
            try:
                id_receiver = (db.execute("SELECT id FROM auth_user WHERE username = " + username)).fetchall()[0]
            except:
                id_receiver = "Error"
            db.execute("INSERT INTO chat(id_receiver) VALUES(?)", id_receiver[0])
    db.close()
    return render(request, "chat_list.html")


def chat_input(request):
    return redirect("https://servusmarket.herokuapp.com/")


def chat_list(request):
    context = get_base_context(request, "Anonuser")
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "chat_list.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "chat_list.html", context)


def room(request):
    """
        chat_room func
        gets request
        returns render of html-page
    """
    if request.method == "POST":
        receiver = request.POST.get('username')
        context = get_base_context(request, receiver)
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "room.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "room.html")


def home(request):
    """
        home page render
        gets request
        returns render of html-page
    """
    context = get_base_context(request, "Anonuser")
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "home.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        db.close()
        return render(request, "home.html", context)


def shopping_cart(request):
    """
        shopping_cart
        gets request
        returns render of html-page
    """

    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        main_username = str(request.user)
        id_product = db.execute("SELECT id_product FROM shopping_cart WHERE main_username = ?",
                                (main_username,)).fetchall()
        if len(id_product) == 0:
            return render(request, "shopping_cart.html")
        else:
            shopping_cart = []
            for i in range(len(id_product)):
                product = (db.execute("SELECT * FROM products WHERE id = ?", id_product[i]).fetchall())[0]
                shopping_cart.append(product)
            db.close()
            return render(request, "shopping_cart.html", {"shopping_cart": shopping_cart})
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_Сonstruction.creating_tables(db)
        main_username = str(request.user)
        id_product = db.execute("SELECT id_product FROM shopping_cart WHERE main_username = ?",
                                (main_username,)).fetchall()
        if len(id_product) == 0:
            return render(request, "shopping_cart.html")
        else:
            shopping_cart = []
            for i in range(len(id_product)):
                product = (db.execute("SELECT * FROM products WHERE id = ?", id_product[i]).fetchall())[0]
                shopping_cart.append(product)
            db.close()
            return render(request, "shopping_cart.html", {"shopping_cart": shopping_cart})


def add_sc(request):
    """
        adding product to shopping cart
        gets request
        returns redirect
    """
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        main_username = str(request.user)
        username = str(form.data["username"])
        with db:
            tr_data = db.execute("SELECT id FROM products WHERE username = ?", (username,)).fetchall()

            id_product = tr_data[0][0]
            arr = (id_product, main_username, username)
            db.execute("INSERT INTO shopping_cart(id_product, main_username, username) VALUES(?, ?, ?)", arr)
        db.close()
        return redirect("https://servusmarket.herokuapp.com/")


def new_product(request):
    """
        adding new products
        gets request
        returns render of html-page
    """
    context = get_base_context(request, "Anonuser")
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = AddProductForm(request.POST)
        label = form.data["label"]
        price = form.data["price"]
        url_img = form.data["url_img"]
        user = str(request.user)
        likes = 0
        id_category = form.data["category"]
        if form.is_valid():
            with db:
                arr = (label, likes, id_category, price, url_img, user)
                db.execute(
                    "INSERT INTO products(label, likes, id_category, price, url_img, username) VALUES(?, ?, ?, ?, ?, ?)",
                    arr)
            context["form"] = form
        return redirect("https://servusmarket.herokuapp.com/")

    else:
        form = AddProductForm()
        context["form"] = form
    db.close()
    return render(request, "new_product.html", context)


def account(request):
    context = get_base_context(request, "Anonuser")
    return render(request, "account.html", context)


class SignUp(CreateView):
    """
        signup func
        gets CreateView
    """
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
