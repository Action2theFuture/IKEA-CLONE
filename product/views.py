from random  import uniform

from django.views   import View
from django.http    import JsonResponse

from product.models import Product, BackgroundImage, Category, SubCategory

class NewListView(View):
    def get(self, request):
        background_images = BackgroundImage.objects.exclude(url="/images/products/null.png")
        new_products      = [
            {
                'id'      : background_image.id,
                'url'     : background_image.url,
                'products': [
                    {
                        'id'          : product.id,
                        'is_new'      : product.is_new,
                        'english_name': product.english_name,
                        'korean_name' : product.korean_name,
                        'sub_category': product.sub_category.korean_name,
                        'price'       : int(product.price)
                    }
                    for product in background_image.product.all()
                ]
            }   
            for background_image in background_images]
        return JsonResponse({'new_products':new_products}, status=200)

class ProductDetailView(View):
    def get(self ,request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'massage':'non-existent product'}, status=404)
            
        product      = Product.objects.get(id=product_id)
        descriptions = product.description.values()
        images_url   = [url['url'] for url in product.image.values('url')]

        result = [
            {
            'id'            : product.id,
            'korean_name'   : product.korean_name,
            'english_name'  : product.english_name,
            'price'         : int(product.price),
            'stock'         : int(product.stock),
            'is_new'        : product.is_new,
            'url'           : [image.url for image in product.image.all()],
            'descriptions'  : list(descriptions),
            'star'          : uniform(0.0,5.0),
            'breadcrumb'    : [
                product.sub_category.category.korean_name, 
                {'id':product.sub_category.id, 
                'name':product.sub_category.korean_name}, 
                product.korean_name]
            }]

        return JsonResponse({'product': result}, status=200)

class RecommendedView(View):
    def get(self, request):
        RECOMMENDED_COUNT = 10
        products = Product.objects.all().order_by('-stock')[:RECOMMENDED_COUNT]
        
        recommended_product= [
            {
                'is_new'           : product.is_new,
                'english_name'     : product.english_name,
                'korean_name'      : product.korean_name,
                'price'            : int(product.price),
                'sub_category_name': product.sub_category.korean_name,
                'star'             : uniform(1.0,5.0),
                'image'            : [
                        image.url
                        for image in product.image.all()[:2]]
            }
            for product in products]
        
        return JsonResponse({'recommended_product':recommended_product}, status=200)

class CategoryView(View):
    def get(self, request):
        category_list     = []
        categorys         = Category.objects.all()

        category_list = [
            {
                'id'          : category.id,
                'korean_name' : category.korean_name,
                'english_name': category.english_name,
                'sub_category': [
                    {
                    'id'          : sub_category.id,
                    'korean_name' : sub_category.korean_name,
                    'english_name': sub_category.english_name
                    }
                for sub_category in SubCategory.objects.filter(category=category)]
            }
            for category in categorys]

        return JsonResponse({'category':category_list}, status=200)
