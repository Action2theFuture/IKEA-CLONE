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
            categorys     = Category.objects.all()
            for category in categorys:
                sub_categorys = list(SubCategory.objects.filter(category=category))
                category_list.append(
                    {
                        'id'          : category.id,
                        'korean_name' : category.korean_name,
                        'english_name': category.english_name,
                        'sub_category': [
                                {
                                    'id'          : s.id,
                                    'korean_name' : s.korean_name,
                                    'english_name': s.english_name
                                } 
                                for s in sub_categorys
                            ]
                    }
                )
            
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
                {
                    'lamp' : {
                        'is_new'      : left_image_lamp.is_new,
                        'english_name': left_image_lamp.english_name,
                        'korean_name' : left_image_lamp.korean_name,
                        'price'       : left_image_lamp.price
                    },
                    'bed' : {
                        'is_new'      : left_image_bed.is_new,
                        'english_name': left_image_bed.english_name,
                        'korean_name' : left_image_bed.korean_name,
                        'price'       : left_image_bed.price
                    },
                    'storage' : {
                        'is_new'      : left_image_storage.is_new,
                        'english_name': left_image_storage.english_name,
                        'korean_name' : left_image_storage.korean_name,
                        'price'       : left_image_storage.price
                    }
                },
                {
                    'lamp' : {
                        'is_new'      : right_image_lamp.is_new,
                        'english_name': right_image_lamp.english_name,
                        'korean_name' : right_image_lamp.korean_name,
                        'price'       : right_image_lamp.price
                    },
                    'bed' : {
                        'is_new'      : right_image_bed.is_new,
                        'english_name': right_image_bed.english_name,
                        'korean_name' : right_image_bed.korean_name,
                        'price'       : right_image_bed.price
                    },
                    'storage' : {
                        'is_new'      : right_image_storage.is_new,
                        'english_name': right_image_storage.english_name,
                        'korean_name' : right_image_storage.korean_name,
                        'price'       : right_image_storage.price
                    }
                }
            ]
            
            return JsonResponse({'category_list':category_list,'recommended':recommend_product, 'new_products':new_products}, status=200)
            
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
                        'korean_name'       : product.korean_name,
                        'english_name'      : product.english_name,
                        'price'             : product.price,
                        'special_price'     : product.special_price,
                        'is_new'            : product.is_new,
                        'color_list'        : [color.name for color in product.color.all()],
                        'sub_cat-egory_name': sub_category.korean_name,
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

            random_number         = random.randrange(1,SubCategory.objects.count()+1)
            recommend_subcategory = SubCategory.objects.get(id=random_number)
            recommend_products    = Product.objects.filter(sub_category=recommend_subcategory).values()

            product_list = []
            product_list.append(
                {
                    'id':product_id.id,
                    'korean_name':product_id.korean_name,
                    'english_name':product_id.english_name,
                    'price':product_id.price,
                    'stock':product_id.stock,
                    'is_new':product_id.is_new,
                    'url':'url',
                    'descriptions':list(descriptions),
                },
            )

            return JsonResponse({'product': product_list,
            'recommend_list': list(recommend_products)
            #'color':color_list, 
            #'images':list(images)
            }, status=200)
        return JsonResponse({'MASSAGE':'Non-existent Product'}, status=404)

class FilterSortView(View):
    def get_queryset(self, request, sub_category_name): 
        sub_category = SubCategory.objects.get(english_name=sub_category_name)
        product_list = Product.objects.filter(sub_category=sub_category)
        return product_list

    def list(self, request, sub_category_name): 
        product_list = self.set_filters(self.get_queryset(request,sub_category_name), request)
        print(product_list)
        return list(product_list.values())

    def set_filters(self, product_list, request): 
        offset = request.GET.get('offset', None) 
        nextoffset = request.GET.get('nextoffset', None)
        if offset is None and nextoffset is None:
            return product_list
        product_list = product_list[int(offset):int(nextoffset)]
        return product_list

    def get(self, request, sub_category_name):
        try:
            field_list = [field.name for field in Product._meta.get_fields()]
            result = []
            sub_category = SubCategory.objects.get(english_name=sub_category_name)
            product_list = Product.objects.filter(sub_category=sub_category)
            sort_list = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}

            print(type(request.GET.keys()))
            if list(request.GET.keys()) == ['offset', 'nextoffset']:
                result.append(FilterSortView.list(self, request, sub_category_name))
            else:
                for key,value in request.GET.items():
                    if key == 'sort':
                        if value not in list(sort_list.keys()):
                            return JsonResponse({'MASSAGE':'INVALID SORT'}, status=404)
                        elif value == 'NEWEST':
                            result.append({key:list(product_list.filter(is_new=True).values())})
                        else:
                            result.append({key:list(product_list.order_by(sort_list[value]).values())})
                        if key not in field_list:
                            raise Product.DoesNotExist 
                        result.append({key:list(Product.objects.filter(**{key:value}).values())})

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist as e:
            return JsonResponse({'MASSAGE':f'{e}'}, status=404)

        except ValidationError as e:
            return JsonResponse({'MASSAGE':f'{e}'}, status=404)

    
