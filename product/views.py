from random import randrange, uniform

from django.views           import View
from django.http            import JsonResponse

from product.models import Category

class RecommendList(View):
    def get(self, request):
        recommend_product  = []
        category_list      = list(Category.objects.all())
        random_number      = randrange(0,len(category_list))
        recommend_category = category_list[random_number]
        sub_categorys      = recommend_category.sub_category
        for sub_category in sub_categorys.all():
            for product in sub_category.product.all():
                images = list(product.image.all().values())
                if images:
                    image_url = images[0]['url']
                recommend_product.append(
                    {
                        'is_new'           : product.is_new,
                        'english_name'     : product.english_name,
                        'korean_name'      : product.korean_name,
                        'price'            : product.price,
                        'sub_category_name': sub_category.korean_name,
                        'image'            : image_url,
                        # 'background_image' : product.image.url,
                        'stars'            : uniform(1.0,5.0)
                    }
                )
        return JsonResponse({'recommend_product':recommend_product}, status=200)