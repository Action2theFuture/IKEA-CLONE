import json

from django.views               import View
from django.http                import JsonResponse, HttpResponse

from product.models import Product, SubCategory

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