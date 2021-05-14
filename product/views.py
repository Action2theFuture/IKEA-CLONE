import json
import random

from django.http  import JsonResponse
from django.views import View

from product.models import *


class MainView(View):
    def get(self, request):
        
        categorys         = Category.objects.all().values('english_name')
        all_category      = {}
        recommend_product = []
        new_products      = {}
        for category in categorys:
            category_name               = category['english_name']
            sub_categorys               = list(SubCategory.objects.filter(category=Category.objects.get(english_name=category_name)).values())  
            all_category[category_name] = [s['english_name'] for s in sub_categorys]
        
        r = random.randrange(1,Category.objects.count()+1)

        recommend_category = Category.objects.get(id=r)
        sub_categorys      = SubCategory.objects.filter(category=recommend_category)

        for sub_category in sub_categorys:
            for product in list(Product.objects.filter(sub_category=sub_category)):
                product_information = {
                    'is_new'       : product.is_new,
                    'english_name' : product.english_name,
                    'korean_name'  : product.korean_name,
                    'price'        : product.price
                }
                recommend_product.append(
                    product_information
                )
        
        

        return JsonResponse({'category':all_category,'recommended':recommend_product}, status=200)
