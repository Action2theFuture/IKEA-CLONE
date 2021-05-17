import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from user.models    import User
from wikea.settings import SECRET_KEY

def authorize(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN' }, status=400)

        except Account.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
    return wrapper