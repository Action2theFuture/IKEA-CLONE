from random import randrange, uniform

from django.views           import View
from django.http            import JsonResponse

from product.models import Category

class RecommendList(View):
    def get(self, request):
        recommend_product  = []
        category_list      = Category.objects.all()
        random_number      = randrange(0,len(category_list))
        recommend_category = category_list[random_number]
        sub_categorys      = recommend_category.sub_category.all()
        recommend_product= [
                {
                    'is_new'           : product.is_new,
                    'english_name'     : product.english_name,
                    'korean_name'      : product.korean_name,
                    'price'            : product.price,
                    'sub_category_name': sub_category.korean_name,
                    'stars'            : uniform(1.0,5.0),
                    'image'            : [
                            image.url
                            for image in product.image.all()[:2]
                        ]
                }
                for sub_category in sub_categorys for product in list(sub_category.product.all())]
        
        return JsonResponse({'recommend_product':recommend_product}, status=200)