from django.views               import View
from django.http                import JsonResponse

from product.models import Category, SubCategory

class CategoryView(View):
    def get(self, request):
        category_list     = []
        sub_category_list = {}
        categorys         = Category.objects.all()

        category_list = [
            {
                'id'          : category.id,
                'korean_name' : category.korean_name,
                'english_name': category.english_name
            }
            for category in categorys
        ]

        for category in categorys:
            sub_category_list[category.korean_name] = [
                {
                    'id'          : sub_category.id,
                    'korean_name' : sub_category.korean_name,
                    'english_name': sub_category.english_name
                }
                for sub_category in SubCategory.objects.filter(category=category)
            ]
        return JsonResponse({'category':category_list,'sub_category':sub_category_list}, status=200)