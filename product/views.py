import json
import random

from django.views               import View
from django.http                import JsonResponse, HttpResponse

from product.models             import Product, SubCategory, Color, Description, Series

class ProductDetailView(View):
    def get(self ,request, pk):
        if Product.objects.filter(id=pk).exists():
            product      = Product.objects.filter(id=pk).values()
            product_id   = Product.objects.get(id=pk)
            descriptions = Description.objects.filter(product=product_id).values()
            color_list   = [color.name for color in product.color.all()]
            images       = Image.objects.filter(product=product).url

            random_number         = random.randrange(1,SubCategory.objects.count()+1)
            recommend_subcategory = SubCategory.objects.get(id=random_number)
            recommend_products    = Product.objects.filter(sub_category=recommend_subcategory).values()

            result = [
                {'id'           : product_id.id,
                'korean_name'   : product_id.korean_name,
                'english_name'  : product_id.english_name,
                'price'         : product_id.price,
                'stock'         : product_id.stock,
                'is_new'        : product_id.is_new,
                'url'           : list(images),
                'descriptions'  : list(descriptions),
                'recommend_list': list(recommend_products),
                'color':color_list, 
                }]
                

            return JsonResponse({'result': result}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent Product'}, status=404)