import json, bcrypt, jwt

from django.views import View
from django.http  import HttpResponse, JsonResponse
from user.models  import User

from wikea.settings import SECRET_KEY

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            log_email    = data['email']
            log_password = data['password'].encode('utf-8')

            if not User.objects.filter(email=log_email).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            user            = User.objects.get(email=log_email)
            user_password   = user.password.encode('utf-8')

            if not bcrypt.checkpw(log_password, user_password):
                return JsonResponse({"MASSAGE": "INVALID_USER"}, status=401)

            data         = {'user_id':user.id}
            access_token = jwt.encode(data, SECRET_KEY, algorithm='HS256')   
            return JsonResponse({'token':access_token}, status=200)

        except KeyError:
            return JsonResponse({'MASSAGE':'KEYERROR'}, status=401)