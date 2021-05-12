import json

from django.views      import View
from django.http     import JsonResponse, HttpResponse

from product.models import product, Category, SubCategory, Color, Description

class ProductView(View):
    def get(self, request, product_id):
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id).values()
            return JsonResponse({'Product':list(product)}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent product'}, status=400)

class ProductMainView(View):
    def get(self, request):
        category_name = Category.obejcts.all().name
        bed           = sub_category 
        return JsonResponse({'Category_name':category_name}, status=200)
