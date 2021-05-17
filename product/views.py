import random

from django.views               import View
from django.http                import JsonResponse
from django.core.exceptions     import ValidationError

from product.models import Product, Category, SubCategory

class Category(View):
    def get(self, request):
        category_list     = []
        sub_category_list = {}
        categorys         = Category.objects.all()
        for category in categorys:
            category_list.append(
                {
                    'id'          : category.id,
                    'korean_name' : category.korean_name,
                    'english_name': category.english_name
                }
            )
            sub_category_list[category.korean_name] = list(SubCategory.objects.filter(category=category).values(
                    'id',
                    'korean_name',
                    'english_name'
                )
            )
        return JsonResponse({'category':category_list,'sub_category':sub_category_list}, status=200)