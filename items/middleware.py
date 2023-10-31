from .models import CartItem, FavoriteItem, Item

from .models import CartItem, FavoriteItem, Item, Cart  # Импортируем модель Cart

class AddToDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Если пользователь авторизован, переносим товары из сессии в базу данных
            cart_items = request.session.pop('cart', [])

            # Проверяем, существует ли корзина пользователя
            cart, created = Cart.objects.get_or_create(user=request.user)

            for item_id in cart_items:
                item = Item.objects.get(id=item_id)
                # Создаем или обновляем запись о товаре в корзине и связываем ее с корзиной
                cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
                cart.items.add(cart_item)  # Добавляем товар в корзину

            favorites = request.session.pop('favorites', [])
            for item_id in favorites:
                item = Item.objects.get(id=item_id)
                favorite_item, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)

        return response