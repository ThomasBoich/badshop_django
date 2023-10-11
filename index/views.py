from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q, Min, Max, F
from users.forms import UserUpdateForm, AddressForm, AddressEditForm, CustomUserSetPasswordForm
from items.models import *
from users.models import Address
from .models import *
from blog.models import *
from django.contrib.auth.forms import PasswordChangeForm  # Добавьте импорт формы смены пароля
from django.contrib.auth import update_session_auth_hash  # Добавьте импорт для обновления сессии после смены пароля
from django.contrib.auth.views import PasswordChangeView
from unidecode import unidecode
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
# Create your views here.

# GLOBAL CONSTANTS
ITEMS = Item.objects.all()
CATEGORIES = Category.objects.all()
SALES = Sale.objects.all()
SLIDER1 = SliderTop.objects.all()
SLIDER2 = SliderTwo.objects.all()
BRENDS = Brend.objects.all()
POSTS = Post.objects.all()

def index(request):
    context = {
        'title': 'Главная страница',
        'items_sails': ITEMS.filter(discount__gt=0),
        'categories': Category.objects.all(),
        'slider1': SliderTop.objects.all(),
        'slider2': SliderTwo.objects.all(),
        'popular_items': Item.objects.all().order_by('-rating'),
        'brends': Brend.objects.all(),
    }
    return render(request, 'index/index.html', context)


def catalog(request):
    context = {
        'title': 'Каталог',
        'categories': Category.objects.all(),
    }
    return render(request, 'index/catalog.html', context)

def catalog_page(request, category_id):
    categories = Category.objects.all()
    minMaxPrice = Item.objects.aggregate(Min('seil_price'), Max('seil_price'))
    minPrice = Item.objects.aggregate(Min('seil_price'))['seil_price__min']
    category = categories.get(id=category_id)
    context = {
        'category': category,
        'items': Item.objects.filter(category_id=category_id),
        'categories': categories,
        'brends': Brend.objects.all(),
        'minMaxPrice': minMaxPrice,
        'minPrice': minPrice,
        'title': f'{category.title}',
    }
    return render(request, 'index/catalogpage.html', context)


# ФИЛЬТРАЦИЯ КАТАЛОГА
def filter(request, category_id=None, items_id=None):
    items = Item.objects.all()
    brends = Brend.objects.all()
    minMaxPrice = Item.objects.aggregate(Min('seil_price'), Max('seil_price'))

    if category_id:
        category = Category.objects.get(id=category_id)

        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))

        context = {
            'category': category,
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
        }

        return render(request, 'index/catalogpage_filter.html', context)

    if items_id:
        category = Category.objects.get(id=category_id)
        items = Item.objects.filter(id=items_id)
        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price))

        context = {
            'category': category,
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
        }

        return render(request, 'index/catalogpage_filter.html', context)

    else:
        # Получение параметров из GET-запроса
        brend = request.GET.getlist("brend")
        min_price = float(request.GET.get("min_price", 0))
        max_price = float(request.GET.get("max_price", 999999))
        search_query = request.GET.get("search", "")

        if brend:
            # Фильтр результатов поиска по бренду и цене
            items = items.filter(
                Q(name__iexact=search_query) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price) & Q(
                    category__title__iexact=search_query) & Q(brend__id__in=brend) & Q(seil_price__gte=min_price) & Q(
                    seil_price__lte=max_price)
            )
        else:
            # Фильтр по бренду, цене, названию товара и категории
            items = items.filter(
                Q(name__iexact=search_query) & Q(seil_price__gte=min_price) & Q(seil_price__lte=max_price)
            )

        context = {
            'items': items,
            'brends': brends,
            'minMaxPrice': minMaxPrice,
            'search_query': search_query,
        }

        return render(request, 'index/catalogpage_filter_search.html', context)


# СТРАНИЦА ТОВАРА
def item(request, item_id):
    items = Item.objects.all()
    item = items.get(id=item_id)
    context = {
        'item': items.get(id=item_id),
        'items': items,
        'certificates': CertificateImages.objects.filter(item=item),
        'title': f'{item.name}',
    }
    return render(request, 'index/item.html', context)

# СТРАНИЦА - БРЕНДЫ
def brends(request):
    context = {
        'brends': Brend.objects.all(),
        'title': 'Бренды'
    }
    return render(request, 'index/brends.html', context)


def pay(request):
    context = {'title': 'Оплата и доставка',}
    return render(request, 'index/pay.html', context)


# СТРАНЦИА АКЦИИ
def sail(request):
    context = {
        'sales': Sale.objects.all(),
        'title': 'Акции',
    }
    return render(request, 'index/sail.html', context)


# СТРАНИЦА ОПРЕДЕЛЕННОЙ АКЦИИ
def salePage(request, sale_id):
    sale = Sale.objects.all().get(id=sale_id)
    context = {
        'sale': sale,
        'title': f'{sale.title}',
    }
    return render(request, 'index/sailpage.html', context)


# СТРАНИЦА О КОМПАНИИ
def about(request):
    context = {'title': 'О  компании',}
    return render(request, 'index/about.html', context)


# СТРАНИЦА ПАРТНЕРЫ
def partners(request):
    context = {
        'partners': Partner.objects.all(),
        'title': 'Партнеры',
    }
    return render(request, 'index/partners.html', context)


# СТРАНИЦА КОНТАКТЫ
def contacts(request):
    context = {'title': 'Контакты',}
    return render(request, 'index/contacts.html', context)


def cabinet(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Мой кабинет',
        }
        return render(request, 'cabinet/cabinet.html', context)
    else:
        return redirect('login')


def favorite(request):
    if request.user.is_authenticated:
        # Если пользователь авторизован, отображаем элементы корзины для этого пользователя
        items = CartItem.objects.filter(user=request.user)
    else:
        # Если пользователь не авторизован, выводим товары из сессии
        try:
            items = CartItem.objects.filter(session=request.session.session_key)
        except:
            items = []
    context = {
        'title': 'Избранные',
        'items': items,
    }
    return render(request, 'cabinet/favorite.html', context)


# СТРАНИЦА МОИ АДРЕСА
def myadress(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddressForm(request.POST, initial={'user': request.user})
            if form.is_valid():
                form.save()
                return redirect('myadress')  # Перенаправление на список адресов после успешного сохранения
        else:
            form = AddressForm(initial={'user': request.user})
            address = Address.objects.filter(users=request.user)
            context = {
                'title': 'Мои адреса',
                'form': form,
                'address': address,
                'address_count': address.count()
            }
        return render(request, 'cabinet/myadress.html', context)
    else:
        return redirect('login')

def delete_address(request, address_id):
    # Получаем адрес по ID или возвращаем 404 ошибку, если адрес не существует
    address = Address.objects.get(pk=address_id)

    # Если запрос выполнен методом POST, удаляем адрес
    address.delete()
    return redirect('myadress')  # Перенаправление на список адресов после удаления


# СТРАНИЦА КОРЗИНЫ
def cart(request):
    if request.user.is_authenticated:
        # Если пользователь авторизован, отображаем элементы корзины для этого пользователя
        items = CartItem.objects.filter(user=request.user)
    else:
        # Если пользователь не авторизован, выводим товары из сессии
        try:
            items = CartItem.objects.filter(session=request.session.session_key)
        except:
            items = []
    context = {
        'items': items,
        'title': 'Корзина',
    }
    return render(request, 'cart/cart.html', context)

def edit_myaddress(request, address_id):
    # Получаем адрес по ID или возвращаем 404 ошибку, если адрес не существует
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        form = AddressEditForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('myadress')  # Перенаправление на список адресов после успешного редактирования
    else:
        form = AddressEditForm(instance=address)

    return render(request, 'cabinet/edit_myadress.html', {'form': form, 'title': address.title})
    


def reset_password(request):

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Обновление сессии после смены пароля
            messages.success(request, 'Пароль успешно изменен.')

            return redirect('my_data')  # Здесь замените 'profile' на имя URL вашего профиля пользователя.

    else:
        password_form = PasswordChangeForm(request.user)


    context = {
        'title': 'Изменение пароля',
        'form': password_form,
        'password_form': password_form,
    }
    return render(request, 'cabinet/reset_password.html', context)


def my_data(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')

            return redirect('my_data')  # Здесь замените 'profile' на имя URL вашего профиля пользователя.
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'title': 'Мои данные',
        'form': form,
    }
    return render(request, 'cabinet/mydata.html', context)


class CustomUserPasswordChangeView(PasswordChangeView):
    form_class = CustomUserSetPasswordForm
    template_name = 'cabinet/reset_password.html'
    success_url = '/cabinet/my_data/'

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)



# @login_required
# def add_to_favorites(request, item_id):
#     item = get_object_or_404(Item, pk=item_id)
#     favorite, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)
#     if created:
#         return JsonResponse({'status': 'added'})
#     else:
#         return JsonResponse({'status': 'already_exists'})

def add_to_session_favorites(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    favorite, created = FavoriteItem.objects.get_or_create(session_id=session_key, item=item)
    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'already_exists'})

@login_required
def remove_from_favorites(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    FavoriteItem.objects.filter(user=request.user, item=item).delete()
    return JsonResponse({'status': 'removed'})

def remove_from_session_favorites(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    session_key = request.session.session_key
    FavoriteItem.objects.filter(session_id=session_key, item=item).delete()
    return JsonResponse({'status': 'removed'})

@login_required
def transfer_session_favorites(request):
    session_key = request.session.session_key
    if not session_key:
        return redirect('cabinet')  # Вернуться на страницу адресов или другую целевую страницу
    favorites = FavoriteItem.objects.filter(session_id=session_key)
    for favorite in favorites:
        FavoriteItem.objects.get_or_create(user=request.user, item=favorite.item)
    return redirect('cabinet')  # Вернуться на страницу адресов или другую целевую страницу


class AddToFavoriteView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        favorites = request.session.get('favorites', [])

        if item_id not in favorites:
            favorites.append(item_id)
            request.session['favorites'] = favorites

            if request.user.is_authenticated:
                FavoriteItem.objects.create(user=request.user, item=item)

        return JsonResponse({'message': 'Товар добавлен в избранное'})

class AddToCartView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        cart = request.session.get('cart', {})

        cart[item_id] = cart.get(item_id, 0) + 1
        request.session['cart'] = cart

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
            cart_item.quantity = (cart_item.quantity if not created else 0) + 1
            cart_item.save()

        return JsonResponse({'message': 'Товар добавлен в корзину'})