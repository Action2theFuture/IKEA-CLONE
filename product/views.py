import json

from django.views               import View
from django.http                import JsonResponse, HttpResponse
from django.db.models.functions import Lower
from django.core.exceptions     import ValidationError
from product.models             import Product, Category, SubCategory, Color, Description, ProductColor, Image, Series

class ProductMainView(View):
    def get(self, request):
        category_values = Category.objects.all().values()
        beds            = Category.objects.get(english_name="beds")
        beds_values     = SubCategory.objects.filter(category=beds).values()
        lamps           = Category.objects.get(english_name="lamps")
        lamps_values    = SubCategory.objects.filter(category=lamps).values()
        storages        = Category.objects.get(english_name="storages")
        storages_values = SubCategory.objects.filter(category=storages).values()
               
        return JsonResponse({
            'category':list(category_values), 
            'bed':list(beds_values), 
            'lighting':list(lamps_values), 
            'bookcase':list(storages_values)}, status=200)

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
                        'color_list'       : [color.name for color in product.color.all()],
                        'sub_category_name': sub_category.korean_name,
                        # 'image'            : Image.objects.get(product=product_id).url
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

            return JsonResponse({
                'product':list(product),
                #'color':color_list, 
                'descriptions':list(descriptions),
                #'images':list(images),
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
            