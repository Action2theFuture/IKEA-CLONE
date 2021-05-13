import json

from django.views      import View
from django.http     import JsonResponse, HttpResponse

from product.models import product, Category, SubCategory, Color, Description, ProductColor, Image, Series

class ProductMainView(View):
    def get(self, request):
        category_values = Category.objects.all().values
        bed             = Category.objects.get(en_name="bed")
        bed_values      = SubCategory.objects.filter(category=bed).values()
        lighting        = Category.objects.get(en_name="Lighting")
        lighting_values = SubCategory.objects.filter(category=lighting).values()
        bookcase        = Category.objects.get(en_name="bookcase")
        bookcase_values = SubCategory.objects.filter(category=bookcase).values()
               
        return JsonResponse({
            'category':list(category_values), 
            'bed':list(bed_values), 
            'lighting':list(lighting_values), 
            'bookcase':list(bookcase_values)}, status=200)

class SubCategoryView(View):
    def get(self, request, category_name):
        if Category.objects.filter(name=category_name).exists():
            category = Category.objects.get(en_name=category_name)
            result   = sub_category.objects.filter(category=category).values()

            return JsonResponse({'result':list(result)}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent CategoryName'}, status=404)

class ProductListView(View):
    def get(self, request, sub_category_name):
        if SubCategory.objects.filter(name=sub_category_name).exists():
            sub_category = SubCategory.objects.get(en_name=sub_category_name)
            product_id   = Product.objects.get(sub_category=sub_category)
            series       = Series.objects.filter(product=product_id).values()
            products     = Product.objects.filter(sub_category=sub_category)

            product_list = []
            for product in products:
                product_list.append(
                    {
                        'ko_name'          : product.ko_name,
                        'en_name'          : product.en_name,
                        'price'            : product.price,
                        'special_price'    : product.special_price,
                        'is_new'           : product.is_new,
                        'color_list'       : [color.name for color in product.color.all()],
                        'sub_category_name': sub_category.ko_name,
                        'image'            : Image.objects.get(product=product_id).url
                    }
                )

            return JsonResponse({'product':product_list},{'series':list(series)}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent SubCategoryName'}, status=404)

class ProductDetailView(View):
    def get(self ,request, product_name):
        if Product.obejcts.filter(name=product_name).exists():
            product            = Product.objects.get(en_name=product_name)
            descriptions       = Description.objects.get(product=product).values()
            color_list         = [color.name for color in product.color.all()]
            images             = Image.objects.get(product=product).url

            return JsonResponse({
                'product':list(product.values()),
                'color':color, 
                'descriptions':list(descriptions),
                'images':list(images)}, status=200)
        return JsonResponse({'MASSAGE':'Non-existent Product'}, status=404)