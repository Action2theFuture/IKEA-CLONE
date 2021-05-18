import json
from random                       import uniform

from django.views                 import View
from django.http                  import JsonResponse
from django.core.exceptions       import ValidationError
from django.db.models.functions   import Lower

from product.models               import Product, SubCategory
from product.sub_product_queryset import get_queryset

class ProductListView(View):
    def get(self, request)
        try:
            sub_category_name = request.GET.get('sub_category_name',None)
            page              = request.GET.get('page',1)
            order_by          = request.GET.get('sort',None)

            sub_category = SubCategory.objects.get(english_name=sub_category_name)

            if sub_category_name is None:
                return JsonResponse({'massage':'non-existent sub_Category_name key'}, status=404)

            series       = [series.english_name for series in product.series.all()]
            products     = get_queryset(request)

            product_count = len(list(products))
            page_count    = product_count//10
            
            last_page     = page_count-1
            VIEW_PRODUCTS = 10
            
            if page_count <= 1:
                products = products

            else:
                if int(page) <= 1:
                    products = products[:VIEW_PRODUCTS]
                else:
                    for page_number in range(page_count):
                        if page_number == last_page:
                            products = products[page_number*VIEW_PRODUCTS:]
                        elif page_number == page:
                            products = products[page_number*VIEW_PRODUCTS:page_number*10+10]

            sort_list    = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}

            if order_by in sort_list.keys():
                if order_by == 'NEWEST':
                    products = products.filter(is_new=True)
                else:
                    products = products.order_by(sort_list[value])

            result = [{ 
                        'id'                : product.id,
                        'korean_name'       : product.korean_name,
                        'english_name'      : product.english_name,
                        'price'             : product.price,
                        'special_price'     : product.special_price,
                        'is_new'            : product.is_new,
                        'color_list'        : [color.name for color in product.color.all()],
                        'sub_category_name' : sub_category.korean_name,
                        'sub_category_url'  : sub_category.english_name,
                        'image'             : [image.url for image in product.image.all()],
                        'series'            : series,
                        'content'           : sub_category.content,
                        'star'              : uniform(0.0,5.0)
                    } for product in products]

            return JsonResponse({'result':result}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)
