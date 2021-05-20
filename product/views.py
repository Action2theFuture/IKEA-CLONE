import json
from random                     import uniform

from django.views               import View
from django.http                import JsonResponse
from django.core.exceptions     import ValidationError

from product.models             import Product

class ProductDetailView(View):
    def get(self ,request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'massage':'non-existent product'}, status=404)
        product      = Product.objects.get(id=product_id)
        descriptions = product.description.values()
        images_url   = [url['url'] for url in product.image.values('url')]

        result = [
            {
            'id'            : product.id,
            'korean_name'   : product.korean_name,
            'english_name'  : product.english_name,
            'price'         : int(product.price),
            'stock'         : product.stock,
            'is_new'        : product.is_new,
            'url'           : [image.url for image in product.image.all()],
            'descriptions'  : list(descriptions),
            'star'          : uniform(0.0,5.0),
            'breadcrumb'    : [
                product.sub_category.category.korean_name, 
                {'id':product.sub_category.id, 
                'name':product.sub_category.korean_name}, 
                product.korean_name]
            }]

        return JsonResponse({'product': result}, status=200)