from django.urls import path

from blog.views import blog, blogPage
from index.views import index, catalog, filter, catalog_page, item, brends, pay, sail, salePage, about, partners, contacts, cabinet, cart, my_data, myadress, \
    delete_address, edit_myaddress, transfer_session_favorites, remove_from_session_favorites, remove_from_favorites, \
    add_to_session_favorites, favorite, CustomUserPasswordChangeView, AddToFavoriteView, AddToCartView
from users.views import AppLoginView, AppLogoutView, AppRegistration

urlpatterns = [

    # ГЛАВНАЯ СТРАНИЦА
    path('', index, name="index"),

    # КАТАЛОГ
    path('catalog/', catalog, name="catalog"),
    path('catalog/category/item/<item_id>/', item, name="item"),
    path('catalog/category/<category_id>/', catalog_page, name="catalog_page"),
    path('catalog/filter/', filter, name="filter_no_category"),
    path('catalog/filter/<category_id>/', filter, name="filter"),

    path('brends/', brends, name="brends"),
    path('pay/', pay, name="pay"),
    path('sale/', sail, name="sail"),
    path('sale/<sale_id>/', salePage, name="salePage"),

    # АУТЕНТИФИКАЦИЯ
    path('login/', AppLoginView.as_view(), name="login"),
    path('logout/', AppLogoutView.as_view(), name="logout"),
    path('registration/', AppRegistration.as_view(), name="registration"),

    # БЛОГ
    path('blog/', blog, name="blog"),
    path('blog/<post_id>/', blogPage, name="blogPage"),

    # ОСТАЛЬНЫЕ СТРАНИЦА
    path('about/', about, name="about"),
    path('partners/', partners, name="partners"),
    path('contacts/', contacts, name="contacts"),

    # ЛИЧНЫЙ КАБИНЕТ
    path('cabinet/', cabinet, name="cabinet"),
    path('cabinet/my_data/', my_data, name="my_data"),
    path('cabinet/reset_password/', CustomUserPasswordChangeView.as_view(), name="reset_password"),
    path('cabinet/my_adress/', myadress, name="myadress"),
    path('cabinet/my_adress/delete_address/<int:address_id>/', delete_address, name='delete_address'),
    path('cabinet/my_adress/edit_myaddress/<int:address_id>/', edit_myaddress, name='edit_myaddress'),
    path('cabinet/favorite/', favorite, name='favorite'),

    # КОРЗИНА
    path('cart/', cart, name="cart"),

    # РАБОТА С КАРЗИНОЙ И ИЗБРАННЫМИ
    #path('add_to_favorites/<int:item_id>/', add_to_favorites, name='add_to_favorites'),
    path('add_to_session_favorites/<int:item_id>/', add_to_session_favorites, name='add_to_session_favorites'),
    path('remove_from_favorites/<int:item_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('remove_from_session_favorites/<int:item_id>/', remove_from_session_favorites, name='remove_from_session_favorites'),
    path('transfer_session_favorites/', transfer_session_favorites, name='transfer_session_favorites'),

    path('add_to_favorites/<int:item_id>/', AddToFavoriteView.as_view(), name='add_to_favorites'),
    path('add_to_cart/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),


]