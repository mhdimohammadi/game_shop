from product.models import Game


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_to_cart(self, game):
        game_id = str(game.id)
        if game_id not in self.cart:
            self.cart[game_id] = {'quantity': 1, 'price': game.get_final_price()}
            self.save()

    def add(self, game):
        game_id = str(game.id)
        if game_id in self.cart:
            self.cart[game_id]['quantity'] += 1
            self.save()

    def decrease(self, game):
        game_id = str(game.id)
        if self.cart[game_id]['quantity'] > 1:
            self.cart[game_id]['quantity'] -= 1
        self.save()

    def remove(self, game):
        game_id = str(game.id)
        if game_id in self.cart:
            del self.cart[game_id]
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def total_price(self):
        price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return price

    def save(self):
        self.session.modified = True

    def __iter__(self):
        game_ids = self.cart.keys()
        games = Game.objects.filter(id__in=game_ids)
        cart_dict = self.cart.copy()
        for game in games:
            cart_dict[str(game.id)]['game'] = game
        for item in cart_dict.values():
            item['total'] = item['price'] * item['quantity']
            yield item
