import json, bcrypt, jwt

from django.views import View
from django.http import HttpResponse, JsonResponse
from user.models import User

from my_settings import SECRET, ALGORITHM

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            password        = data['password']
            user            = User.objects.get(email=data['email'])
            hashed_password = user.password.encode('utf-8')

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return JsonResponse({"MASSAGE": "INVALID_USER"}, status=401)

            data         = {'user_id':user.id}
            access_token = jwt.encode(data, SECRET, algorithm=ALGORITHM)   
            return JsonResponse({'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MASSAGE':'KEYERROR'}, status=401)