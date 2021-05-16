import json
import random

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.models.functions import Lower
from django.core.exceptions     import ValidationError

from product.models import Product, Category, SubCategory, Color, Description, ProductColor, Image, Series

class MainView(View):
    def get(self, request):
        try:
            # 카테고리, 세부 카테고리
            category_list = []
            sub_category_list = {}
            categorys     = Category.objects.all()
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
                        'id'          : s.id,
                        'korean_name' : s.korean_name,
                        'english_name': s.english_name
                    } 
                    for s in sub_categorys
                ]
                
            
            # 추천 상품
            recommend_product  = []
            random_nember      = random.randrange(1,Category.objects.count()+1)
            recommend_category = Category.objects.get(id=random_nember)
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

            # 신상품
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
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SubCategoryView(View):
    def get(self, request, category_name):
        if Category.objects.filter(english_name=category_name).exists():
            category = Category.objects.get(english_name=category_name)
            result   = SubCategory.objects.filter(category=category).values()

            return JsonResponse({'result':list(result)}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent CategoryName'}, status=404)

class ProductListView(View):
    def get(self, request, sub_category_name):
        if SubCategory.objects.filter(english_name=sub_category_name).exists():
            sub_category = SubCategory.objects.get(english_name=sub_category_name)
            product_id   = Product.objects.get(sub_category=sub_category)
            series       = product_id.series.english_name
            products     = Product.objects.filter(sub_category=sub_category)

            product_list = []
            for product in products:
                product_list.append(
                    {
                        'korean_name'          : product.ko_name,
                        'english_name'          : product.english_name,
                        'price'            : product.price,
                        'special_price'    : product.special_price,
                        'is_new'           : product.is_new,
                        'color_list'       : [color.name for color in product.color.all()],
                        'sub_cat-egory_name': sub_category.ko_name,
                        # 'image'            : Image.objects.get(product=product_id).url
                        'star':2
                    }
                )

            return JsonResponse({'product':product_list,'series':series}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent SubCategoryName'}, status=404)

class ProductDetailView(View):
    def get(self ,request, product_name):
        if Product.objects.filter(english_name=product_name).exists():
            product            = Product.objects.filter(english_name=product_name).values()
            product_id         = Product.objects.get(english_name=product_name)
            descriptions       = Description.objects.filter(product=product_id).values()
            #color_list         = [color.name for color in product.color.all()]
            #images             = Image.objects.get(product=product).url
            product_list = []
            product_list.append(
                {
                    'id':product_id.id,
                    'korean_name':product_id.korean_name,
                    'english_name':product_id.english_name,
                    'stock':product_id.stock,
                    'is_new':product_id.is_new,
                    'url':'url',
                    'descriptions':list(descriptions),
                },
            )
            return JsonResponse({'product': product_list,
            #'color':color_list, 
            #'images':list(images)
            }, status=200)
        return JsonResponse({'MASSAGE':'Non-existent Product'}, status=404)

class FilterSortView(View):
    def get(self, request, sub_category_name):
        try:
            field_list = [field.name for field in Product._meta.get_fields()]
            result = []
            sort_list = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}
            for key,value in request.GET.items():
                if key == 'sort':
                    if value not in list(sort_list.keys()):
                        return JsonResponse({'MASSAGE':'INVALID SORT'}, status=404)
                    result.append({key:list(Product.objects.all().order_by(sort_list[value]).values())})
                else:
                    if key not in field_list:
                        raise Product.DoesNotExist 
                    result.append({key:list(Product.objects.filter(**{key:value}).values())})
            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist as e:
            return JsonResponse({'MASSAGE':f'{e}'}, status=404)
            
        except ValidationError as e:
            return JsonResponse({'MASSAGE':f'{e}'}, status=404)