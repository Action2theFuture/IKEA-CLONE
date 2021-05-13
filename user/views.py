import json
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View

from wikea.settings import SECRET_KEY
from user.models    import User
from user.validate  import validate_email, validate_password

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            first_name   = data['first_name']
            last_name    = data['last_name']
            email        = data['email']
            birthday     = data['birthday']
            phone_number = data['phone_number']
            password     = data['password']

            if not validate_email(email):
                return JsonResponse({'message':'IMVALID EMAIL'}, status=400)
            
            if not validate_password(password):
                return JsonResponse({'message':'IMVALID PASSWORD'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            if User.objects.filter(first_name = first_name, last_name = last_name).exists():
                return JsonResponse({'message':'DUPLICATE NAME'}, status=409)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'DUPLICATE EMAIL'}, status=409)

            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message':'DUPLICATE PHONE_NUMBER'}, status=409)
            
            User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                birthday     = birthday,
                phone_number = phone_number,
                password     = hashed_password
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)