import random

from django.views               import View
from django.http                import JsonResponse
from django.core.exceptions     import ValidationError

from product.models import Product, Category, SubCategory

class Main(View):
    def post(self, request):
        category_list     = []
        sub_category_list = {}
        categorys         = Category.objects.all()
        for category in categorys:
            sub_categorys = list(SubCategory.objects.filter(category=category))
            category_list.append(
                {
                    'id'          : category.id,
                    'korean_name' : category.korean_name,
                    'english_name': category.english_name
                }
            )
            sub_category_list[category.korean_name] = [
                {
                    'id'          : sub_category.id,
                    'korean_name' : sub_category.korean_name,
                    'english_name': sub_category.english_name
                } 
                for sub_category in sub_categorys
            ]
        return JsonResponse({'category':category_list,'sub_category':sub_category_list}, status=200)

    def get(self, request):
            # 추천 상품
            recommend_product  = []
            random_number      = random.randrange(1,Category.objects.count()+1)
            recommend_category = Category.objects.get(id=random_number)
            sub_categorys      = SubCategory.objects.filter(category=recommend_category)

            for sub_category in sub_categorys:
                for product in list(Product.objects.filter(sub_category=sub_category)):
                    recommend_product.append(
                        {
                            'is_new'       : product.is_new,
                            'english_name' : product.english_name,
                            'korean_name'  : product.korean_name,
                            'price'        : product.price
                        }
                    )

            # 신상품(정해진 Product)
            new_products        = [] # 신상품
            left_image_lamp     = Product.objects.get(english_name="nikelamp")
            left_image_bed      = Product.objects.get(english_name="nikebed")
            left_image_storage  = Product.objects.get(english_name="nikestorage")
            right_image_lamp    = Product.objects.get(english_name="adidaslamp")
            right_image_bed     = Product.objects.get(english_name="adidasbed")
            right_image_storage = Product.objects.get(english_name="adidasstorage")
            new_products = [
                [             
                    {
                        'id'          : left_image_lamp.id,
                        'is_new'      : left_image_lamp.is_new,
                        'english_name': left_image_lamp.english_name,
                        'korean_name' : left_image_lamp.korean_name,
                        'sub_category': left_image_lamp.sub_category.korean_name,
                        'price'       : left_image_lamp.price
                    },
                    {
                        'id'          : left_image_bed.id,
                        'is_new'      : left_image_bed.is_new,
                        'english_name': left_image_bed.english_name,
                        'korean_name' : left_image_bed.korean_name,
                        'sub_category': left_image_bed.sub_category.korean_name,
                        'price'       : left_image_bed.price
                    },
                    {
                        'id'          : left_image_storage.id,
                        'is_new'      : left_image_storage.is_new,
                        'english_name': left_image_storage.english_name,
                        'korean_name' : left_image_storage.korean_name,
                        'sub_category': left_image_storage.sub_category.korean_name,
                        'price'       : left_image_storage.price
                    }
                ]
                ,
                [
                    {
                        'id'          : right_image_lamp.id,
                        'is_new'      : right_image_lamp.is_new,
                        'english_name': right_image_lamp.english_name,
                        'korean_name' : right_image_lamp.korean_name,
                        'sub_category': right_image_lamp.sub_category.korean_name,
                        'price'       : right_image_lamp.price
                    },
                    {
                        'id'          : right_image_bed.id,
                        'is_new'      : right_image_bed.is_new,
                        'english_name': right_image_bed.english_name,
                        'korean_name' : right_image_bed.korean_name,
                        'sub_category': right_image_bed.sub_category.korean_name,
                        'price'       : right_image_bed.price
                    },
                    {
                        'id'          : right_image_storage.id,
                        'is_new'      : right_image_storage.is_new,
                        'english_name': right_image_storage.english_name,
                        'korean_name' : right_image_storage.korean_name,
                        'sub_category': right_image_storage.sub_category.korean_name,
                        'price'       : right_image_storage.price
                    }
                ]
            ]
            
            return JsonResponse({'category_list':category_list,'sub_category_list':sub_category_list,'recommended':recommend_product, 'new_products':new_products}, status=200)