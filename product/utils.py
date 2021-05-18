from product.models import BackgroundImage

def get_background():
    return BackgroundImage.objects.get_or_create(url="null")

def get_background_id():
    return get_background().id