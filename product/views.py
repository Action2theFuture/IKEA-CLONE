import json
import random

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.models.functions import Lower
from django.core.exceptions     import ValidationError
from product.models             import Product, Category, SubCategory, Color, Description, ProductColor, Image, Series


class MainView(View):
    def get(self, request):
        categorys         = Category.objects.all().values('english_name')
        all_category      = {}
        recommend_product = []
        new_products      = {}
        for category in categorys:
            category_name               = category['english_name']
            sub_categorys               = list(SubCategory.objects.filter(category=Category.objects.get(english_name=category_name)).values())  
            all_category[category_name] = [s['english_name'] for s in sub_categorys]
        
        r = random.randrange(1,Category.objects.count()+1)

        recommend_category = Category.objects.get(id=r)
        sub_categorys      = SubCategory.objects.filter(category=recommend_category)

        for sub_category in sub_categorys:
            for product in list(Product.objects.filter(sub_category=sub_category)):
                product_information = {
                    'is_new'       : product.is_new,
                    'english_name' : product.english_name,
                    'korean_name'  : product.korean_name,
                    'price'        : product.price
                }
                recommend_product.append(
                    product_information
                )
        
        

        return JsonResponse({'category':all_category,'recommended':recommend_product}, status=200)

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
                        'ko_name'          : product.korean_name,
                        'en_name'          : product.english_name,
                        'price'            : product.price,
                        'special_price'    : product.special_price,
                        'is_new'           : product.is_new,
                        #'color_list'       : [color.name for color in product.color.all()],
                        'sub_category_name': sub_category.korean_name,
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