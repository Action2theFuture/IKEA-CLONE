import json

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.models.functions import Lower
from django.core.exceptions     import ValidationError

from product.models             import Product, SubCategory

class ProductListView(View):
    def get_queryset(self, request, sub_category_name): 
        sub_category = SubCategory.objects.get(english_name=sub_category_name)
        product_list = Product.objects.filter(sub_category=sub_category)
        return product_list

    def list(self, request, sub_category_name): 
        product_list = self.set_filters(self.get_queryset(request,sub_category_name), request)
        return list(product_list.values())

    def set_filters(self, product_list, request): 
        offset     = request.GET.get('offset', None)
        nextoffset = request.GET.get('nextoffset', None)

        if (offset != "") and (nextoffset != ""):
            product_list = product_list[int(offset):int(nextoffset)]
            return product_list

        if offset == "":
            product_list = product_list[:int(nextoffset)]
            return product_list
            
        if nextoffset == "":
            product_list = product_list[int(offset):]
            return product_list

    def get(self, request, sub_category_name):
        try:
            if list(request.GET.keys()) != []:
                field_list   = [field.name for field in Product._meta.get_fields()]
                result       = []
                sub_category = SubCategory.objects.get(english_name=sub_category_name)
                product_list = Product.objects.filter(sub_category=sub_category)
                sort_list    = {'PRICE_LOW_TO_HIGH':'price','PRICE_HIGH_TO_LOW':'-price','NEWEST':'is_new','NAME_ASCENDING':Lower('ko_name')}

                #pagenation 
                if list(request.GET.keys()) == ['offset', 'nextoffset']:
                    result.append(ProductListView.list(self, request, sub_category_name))

                else:
                    #정렬 filter
                    for key, value in request.GET.items():
                        if key == 'sort':
                            if value not in list(sort_list.keys()):
                                return JsonResponse({'massage':'INVALID SORT'}, status=404)

                            elif value == 'NEWEST':
                                result.append(product_list.filter(is_new=True).values())
                            else:
                                result.append(product_list.order_by(sort_list[value]).values())

                        #색상, 가격, 시리즈, 특가, 신제품 filter(가격대 filter code 추가 필요)
                        elif key != 'sort':
                            if key not in field_list:
                                raise Product.DoesNotExist 
                            else:
                                result.append(product_list.filter(**{key:value}).values())
                
                result = [list(i.values()) for i in result]     
                return JsonResponse({'result':result}, status=200)

            else:
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
                return JsonResponse({'massage':'Non-existent SubCategoryName'}, status=404)
        
        except Product.DoesNotExist as e:
            return JsonResponse({'massage':f'{e}'}, status=404)

        except ValidationError as e:
            return JsonResponse({'massge':f'{e}'}, status=404)

                        