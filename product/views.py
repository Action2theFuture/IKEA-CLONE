import random

from django.views           import View
from django.http            import JsonResponse

from product.models import Product, Category, SubCategory

class RecommendList(View):
    def get(self, request):
        recommend_product  = []
        category_list      = list(Category.objects.all())
        random_number      = random.randrange(0,len(category_list))
        recommend_category = category_list[random_number]
        sub_categorys      = list(recommend_category.sub_category)
        for sub_category in sub_categorys:
            recommend_product.append(
                {
                    'is_new'          : product.is_new,
                    'english_name'    : product.english_name,
                    'korean_name'     : product.korean_name,
                    'price'           : product.price,
                    'image'           : product.image[0].url,
                    'background_image': product.image[1].url
                }
                for product in sub_category.product
            )
        return JsonResponse({'recommend_product':recommend_product}, status=200)