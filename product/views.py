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
                descriptions = product.description.values()
                images_url   = product.image.values('url')

                result = [
                    {
                    'id'            : product.id,
                    'korean_name'   : product.korean_name,
                    'english_name'  : product.english_name,
                    'price'         : product.price,
                    'stock'         : product.stock,
                    'is_new'        : product.is_new,
                    'url'           : list(images_url),
                    'descriptions'  : list(descriptions),
                    'star'          : uniform(0.0,5.0),
                    'breadcrumb'    : [
                        product.sub_category.category.korean_name, 
                        {'id':product.sub_category.id, 
                        'name':product.sub_category.korean_name}, 
                        product.korean_name]
                    }]
                    

            return JsonResponse({'product': result}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)