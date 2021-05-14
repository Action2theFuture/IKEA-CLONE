import json, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from wikea.settings import SECRET_KEY
from user.models    import User
from user.validate  import validate_email, validate_password

class Signup(View):
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
            
            if User.objects.filter(first_name = first_name, last_name = last_name).exists():
                return JsonResponse({'message':'DUPLICATE NAME'}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'DUPLICATE EMAIL'}, status=400)

            if User.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'message':'DUPLICATE PHONE_NUMBER'}, status=400)

            User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                birthday     = birthday,
                phone_number = phone_number,
                password     = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)

class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            log_email    = data['email']
            log_password = data['password'].encode('utf-8')

            if not User.objects.filter(email=log_email).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

            user            = User.objects.get(email=log_email)
            user_password   = user.password.encode('utf-8')

            if not bcrypt.checkpw(log_password, user_password):
                return JsonResponse({'MASSAGE': 'INVALID_USER'}, status=401)

            data         = {'user_id':user.id}
            access_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')   
            return JsonResponse({'MESSAGE':'SUCCESS' , 'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MASSAGE':'KEYERROR'}, status=400)
