import jwt

from django.http  import JsonResponse

from user.models import User
from wikea.settings import SECRET_KEY

def authorize(func):
    
    def wrapper():
        if not access_token:
            return JsonResponse({'MESSAGE': 'NECCESSARY LOGIN'}, status=403)

        header = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')

        if not User.objects.filter(id = header['user_id']).exists():
            return JsonResponse({'MESSAGE': 'UNAUTHORIZED USER'}, status=403)
        else:
            func()

    return wrapper()