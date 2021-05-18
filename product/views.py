from django.views   import View
from django.http    import JsonResponse

from product.models import Product, BackgroundImage

class NewListView(View):
    def get(self, request):
        new_products      = []
        background_images = BackgroundImage.objects.all()
        for background_image in background_images:
            new_products.append(
                {
                    'id'      : background_image.id,
                    'src'     : background_image.url,
                    'products': {
                        'id'          : product.id,
                        'is_new'      : product.is_new,
                        'english_name': product.english_name,
                        'korean_name' : product.korean_name,
                        'price'       : product.price
                    }   
                }
                for product in Product.objects.filter(background_image = background_image)
            )
        return JsonResponse({'new_products':new_products}, status=200)