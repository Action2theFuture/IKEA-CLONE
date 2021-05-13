import json

from django.http  import JsonResponse
from django.views import View

from product.models import *


class MainView(View):
    def get(self, request):
        categorys      = Category.objects.all()
        category_names = categorys.values('english_name')
        print(list(category_names))


        new_products = {}
        products = Product.objects.all()
        for category in categorys:
            category_name = category.english_name
            sub_categorys = SubCategory.objects.filter(category = category)
            new_products[category_name] = []
            for sub_category in sub_categorys:
                new_products[category_name].append(list(Product.objects.filter(sub_category=sub_category, is_new=True).values('english_name')))
        return JsonResponse({'category':list(category_names), 'new_products':new_products}, status=200)