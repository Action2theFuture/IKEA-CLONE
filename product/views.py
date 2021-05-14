import json

from django.http  import JsonResponse
from django.views import View

from product.models import *


class MainView(View):
    def get(self, request):
        categorys = Category.objects.all().values('english_name')
        all_category = {}
        for category in categorys:
            category_name = category['english_name']
            sub_categorys = list(SubCategory.objects.filter(category=Category.objects.get(english_name=category_name)).values())
            for sub_category in sub_categorys:
                all_category[category_name] = [s['english_name'] for s in sub_categorys]
        
        return JsonResponse({'category':all_category}, status=200)