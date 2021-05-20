from random import uniform

from django.views           import View
from django.http            import JsonResponse

from product.models import Product

class RecommendedView(View):
    def get(self, request):
        RECOMMENDED_COUNT = 10
        products = Product.objects.all().order_by('-stock')[:RECOMMENDED_COUNT]
        
        recommended_product= [
                {
                    'is_new'           : product.is_new,
                    'english_name'     : product.english_name,
                    'korean_name'      : product.korean_name,
                    'price'            : product.price,
                    'sub_category_name': product.sub_category.korean_name,
                    'star'             : uniform(1.0,5.0),
                    'image'            : [
                            image.url
                            for image in product.image.all()[:2]]
                }
                for product in products]
        
        return JsonResponse({'recommended_product':recommended_product}, status=200)