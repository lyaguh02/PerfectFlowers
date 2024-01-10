from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # при отсутствии значений, создаем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """
        Возвращает сгенерированный список товаров из корзины
        """
        for id_ in self.cart.keys():
            self.cart[str(id_)]['product'] = Product.objects.get(id=id_)

        for item in self.cart.values():
            item['total_price'] = Decimal(item['product'].price * item['quantity'])

            yield item

    def __len__(self):
        """
        Возвращает количество товаров находящихся в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляет товар в корзину или обновляет его количество
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': int(product.price)}
        if update_quantity:
            if quantity <= 0:
                self.remove(product_id)
            else:
                self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product_id):
        """
        Удаляет товар из корзины
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Сохраняет текущую сессию
        """
        self.session.modified = True

    def clear(self):
        """
        Очищает корзину
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def total_price(self):
        """
        Возвращает общую стоимость корзины
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
