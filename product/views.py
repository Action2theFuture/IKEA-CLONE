import json
from random                     import uniform

from django.views               import View
from django.http                import JsonResponse
from django.core.exceptions     import ValidationError

from product.models             import Product

class ProductDetailView(View):
    def get(self ,request):
        try:
            pk = request.GET.get('id',None)

            if pk is not None:
                product_list = Product.objects.filter(id=pk).values()
                product      = Product.objects.get(id=pk)
                descriptions = Product.description.filter(product=product).values()
                color_list   = [color.name for color in product.color.all()]
                images_url   = Product.image.filter(product=product).url

                result = [
                    {'id'           : product.id,
                    'korean_name'   : product.korean_name,
                    'english_name'  : product.english_name,
                    'price'         : product.price,
                    'stock'         : product.stock,
                    'is_new'        : product.is_new,
                    'url'           : list(images_url),
                    'descriptions'  : list(descriptions),
                    'color'         : color_list, 
                    'star'          : uniform(0.0,5.0)
                    }]
                    

            return JsonResponse({'result': result}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)