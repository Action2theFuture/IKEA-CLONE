from product.models import Product, SubCategory

def get_queryset(self, request):
    sub_category_name = request.GET.get('sub_category_name',None) 
    if sub_category_name is not None:
        sub_category = SubCategory.objects.get(english_name=sub_category_name)
        product_list = Product.objects.filter(sub_category=sub_category)
        return product_list