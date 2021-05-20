import json
import operator
import functools
import math 

from random                       import uniform

from django.views                 import View
from django.http                  import JsonResponse
from django.core.exceptions       import ValidationError
from django.db.models             import Q
from django.db.models.functions   import Lower

from product.models               import Product, Series, Category, SubCategory
from product.sub_product_queryset import get_queryset

class ProductListView(View):
    def get(self, request):
        try:
            sub_category_name = request.GET.get('sub_category_name',None)
            page              = int(request.GET.get('page',1))
            order_by          = request.GET.get('sort',None)

            if not sub_category_name:
                return JsonResponse({'massage':'non-existent sub_Category_name key'}, status=404)

            products     = get_queryset(request)

            sort_list    = {'PRICE_LOW_TO_HIGH':'price',
                            'PRICE_HIGH_TO_LOW':'-price',
                                       'NEWEST':'is_new',
                               'NAME_ASCENDING':Lower('english_name')}
            #정렬 기능
            if order_by in sort_list.keys():
                if order_by == 'NEWEST':
                    products = products.filter(is_new=True)
                else:
                    products = products.order_by(sort_list[order_by])
            #필터 기능
            fields      = [field.name for field in Product._meta.get_fields()]
            predicates  = []
            
            for field in fields:
                key   = field
                value = request.GET.get(field)
                if value:
                    if key == 'price':
                        min_price, max_price = value.split('-')
                        products = products.filter(price__gte=min_price, price__lte=max_price)
                    else:
                        predicates.append((key,value))
            queryList = [Q(x) for x in predicates]

            if queryList:
                products = products.filter(functools.reduce(operator.and_, queryList))
            #페이지네이션 기능
            product_count = len(list(products))
            VIEW_PRODUCTS = 8
            page_count    = math.ceil(product_count/VIEW_PRODUCTS)
            last_page     = page_count
            
            for page_number in range(1, page_count+1):
                if page == 1:
                    products = products[:VIEW_PRODUCTS]
                else:
                    if page == last_page:
                        products = products[(page_number-1)*VIEW_PRODUCTS:]
                    else:
                        products = products[(page_number-1)*VIEW_PRODUCTS:page_number*VIEW_PRODUCTS+VIEW_PRODUCTS]
                        
            result = [{ 
                        'id'                : product.id,
                        'korean_name'       : product.korean_name,
                        'english_name'      : product.english_name,
                        'price'             : int(product.price),
                        'special_price'     : int(product.special_price),
                        'is_new'            : product.is_new,
                        'color_list'        : [color.korean_name for color in product.color.all()],
                        'sub_category_name' : product.sub_category.korean_name,
                        'sub_category_url'  : product.sub_category.english_name,
                        'image'             : [image.url for image in product.image.all()],
                        'series'            : product.series.korean_name,
                        'content'           : product.sub_category.content,
                        'star'              : uniform(0.0,5.0)
                    } for product in products]

            return JsonResponse({'product':result}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)
        
        except KeyError:
            return JsonResponse({'massage':'keyerror'}, status=404)

class RecommendedView(View):
    def get(self, request):
        RECOMMENDED_COUNT = 10
        products = Product.objects.all().order_by('-stock')[:RECOMMENDED_COUNT]
        
        recommended_product= [
                {
                    'is_new'           : product.is_new,
                    'english_name'     : product.english_name,
                    'korean_name'      : product.korean_name,
                    'price'            : int(product.price),
                    'sub_category_name': product.sub_category.korean_name,
                    'star'             : uniform(1.0,5.0),
                    'image'            : [
                            image.url
                            for image in product.image.all()[:2]]
                }
                for product in products]
        
        return JsonResponse({'recommended_product':recommended_product}, status=200)

class CategoryView(View):
    def get(self, request):
        category_list     = []
        categorys         = Category.objects.all()

        category_list = [
            {
                'id'          : category.id,
                'korean_name' : category.korean_name,
                'english_name': category.english_name,
                'sub_category': [
                    {
                    'id'          : sub_category.id,
                    'korean_name' : sub_category.korean_name,
                    'english_name': sub_category.english_name
                    }
                for sub_category in SubCategory.objects.filter(category=category)]
            }
            for category in categorys]

        return JsonResponse({'category':category_list}, status=200)
