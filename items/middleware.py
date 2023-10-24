from .models import CartItem, FavoriteItem, Item

class AddToDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Если пользователь авторизован, переносим товары из сессии в базу данных
            cart = request.session.pop('cart', [])

            for item_id in cart:
                item = Item.objects.get(id=item_id)
            # for item_id, quantity in cart.items():
            #     item = Item.objects.get(id=item_id)
                cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
                # cart_item.quantity += quantity
                cart_item.save()

            favorites = request.session.pop('favorites', [])
            for item_id in favorites:
                item = Item.objects.get(id=item_id)
                favorite_item, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)

        return response