from product.models               import Product, SubCategory

from django.core.exceptions       import ValidationError

def get_queryset(request):
    try:
        sub_category_name = request.GET.get('sub_category_name',None) 
        if sub_category_name:
            sub_category = SubCategory.objects.get(english_name=sub_category_name)
            product_list = Product.objects.filter(sub_category=sub_category)
            return product_list

    except ValidationError as e:
            return JsonResponse({'massage':f'{e}'}, status=404)