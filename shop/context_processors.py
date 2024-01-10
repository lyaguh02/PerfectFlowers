from .cart import Cart
from .models import Category


def extras(request):
    """Здесь задаются переменные для всех шаблонов"""
    return {"categories": Category.objects.all(),
            "cart": Cart(request)}
