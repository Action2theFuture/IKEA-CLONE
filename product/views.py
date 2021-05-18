import json

from django.views                 import View
from django.http                  import JsonResponse
from django.core.exceptions       import ValidationError

from product.models               import Product, SubCategory
from product.sub_product_queryset import get_queryset

class ProductListView(View):
    def get(self, request)
        try:
            sub_category_name = request.GET.get('sub_category_name',None)

            if pk is not None:
                series       = [series.english_name for series in product.series.all()]
                products     = get_queryset(self, request)

                result = [{
                            'korean_name'       : product.korean_name,
                            'english_name'      : product.english_name,
                            'price'             : product.price,
                            'special_price'     : product.special_price,
                            'is_new'            : product.is_new,
                            'color_list'        : [color.name for color in product.color.all()],
                            'sub_cat-egory_name': sub_category.korean_name,
                            'image'             : [image.url for image in product.image.all()],
                            'series'            : series,
                            'content'           : sub_category.content
                        } for product in products]

                return JsonResponse({'result':result}, status=200)
                
        except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)