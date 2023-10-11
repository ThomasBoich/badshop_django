from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from items.forms import AddItemForm, ItemImageForm
from items.models import Item, FavoriteItem, CartItem

# Create your views here.
# class CreateItem(View):
#     template_name = 'bulletinboard/add_advert.html'
#     form_class = AddItemForm
#     form_images_class = ItemImageForm
#     model = Item
#
#     def get(self, request):
#         form = self.form_class()
#         form_images = self.form_images_class()
#         return render(request, self.template_name, {'form': form, 'form_images': form_images})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         form_images = self.form_images_class(request.POST, request.FILES, request=request)
#         if form.is_valid() and form_images.is_valid():
#             advert = form.save()
#             form_images.save_for(advert)
#             return HttpResponseRedirect('/')
#         return render(request, self.template_name, {'form': form, 'form_images': form_images})


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

@login_required
def add_to_favorites(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    favorite, created = FavoriteItem.objects.get_or_create(user=request.user, item=item)
    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'already_exists'})

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







from django.http import JsonResponse

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