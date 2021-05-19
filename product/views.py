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

from product.models               import Product, SubCategory, Series
from product.sub_product_queryset import get_queryset

class ProductListView(View):
    def get(self, request):
        try:
            sub_category_name = request.GET.get('sub_category_name',None)
            page              = int(request.GET.get('page',1))
            order_by          = request.GET.get('sort',None)

            sub_category = SubCategory.objects.get(english_name=sub_category_name)

            if sub_category_name is None:
                return JsonResponse({'massage':'non-existent sub_Category_name key'}, status=404)

            products     = get_queryset(request)

            sort_list    = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}

            if order_by in sort_list.keys():
                if order_by == 'NEWEST':
                    products = products.filter(is_new=True)
                else:
                    products = products.order_by(sort_list[order_by])
            


            series_list = [series.english_name for series in Series.objects.all()]
            fields      = [field.name for field in Product._meta.get_fields()]
            predicates  = []

            print(fields)
            for field in fields:
                key   = field
                value = request.GET.get(field)
                print(value)
                if value:
                    predicates.append((key,value))
            queryList = [Q(x) for x in predicates]

            print(queryList)
            if not queryList:
                products = products.filter(functools.reduce(operator.and_, queryList))

            product_count = len(list(products))
            page_count    = math.ceil(product_count/8)
            last_page     = page_count
            VIEW_PRODUCTS = 8
            
            for page_number in range(1, page_count+1):
                if page == 1:
                    products = products[:VIEW_PRODUCTS]
                elif page_number == page:
                    products = products[(page_number-1)*VIEW_PRODUCTS:page_number*VIEW_PRODUCTS+VIEW_PRODUCTS]
                if last_page > 2:
                    if page == last_page:
                        products = products[(page_number-1)*VIEW_PRODUCTS:]

            result = [{ 
                        'id'                : product.id,
                        'korean_name'       : product.korean_name,
                        'english_name'      : product.english_name,
                        'price'             : product.price,
                        'special_price'     : product.special_price,
                        'is_new'            : product.is_new,
                        'color_list'        : [color.name for color in products.color.all()],
                        'sub_category_name' : sub_category.korean_name,
                        'sub_category_url'  : sub_category.english_name,
                        'image'             : [image.url for image in list(product.image.all())],
                        'series'            : product.series.korean_name,
                        'content'           : sub_category.content,
                        'star'              : uniform(0.0,5.0)
                    } for product in products]

            return JsonResponse({'product':result}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)
        
        except KeyError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)