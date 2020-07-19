import json
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View

from users.models   import User,Following
from my_settings    import SECRET_KEY
from utils          import login_decorator

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['email'] and data['password']:

                if '@' not in data['email']:
                    return JsonResponse({'message':'Invalid email format'}, status=401)

                if User.objects.filter(email=data['email']).exists():
                    return JsonResponse({'message':'Already registered User_ID'}, status=401)

                if len(data['password']) < 5:
                    return JsonResponse({'message':'Password must be at least 5 chracters.'}, status=401)

                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                hashed_password = hashed_password.decode('utf-8')
                User(
                    #name    = data['name'],
                    name     = "fake",
                    email    = data['email'],
                    password = hashed_password
                ).save()
                return JsonResponse({'message':'Register Success'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)

        if User.objects.filter(email=data['email']).exists():
            login_user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'),login_user.password.encode('utf-8')):
                secret_code     =   SECRET_KEY['secret']
                access_token    =   jwt.encode({'id' : login_user.id}, secret_code , algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode('utf-8')}, status=200)

            return JsonResponse({'message':'INVALID ID or PASSWORD'}, status=401)

        return JsonResponse({'message':'INVALID ID or PASSWORD'}, status=401)

class FollowUserView(View):

    @login_decorator
    def post(self,request):
        data    =   json.loads(request.body)
        user_id =   request.user.id

        try:
            if User.objects.filter(id=data['followed_user_id']).exists():
                following_users = list(Following.objects.filter(followed_user=data['followed_user_id']).values('following_user_id'))

                for following_user in following_users:
                    if user_id  ==  following_user['following_user_id']:
                        return JsonResponse({'message':'Already Followed'}, status=401)

                Following(
                        followed_user_id     =   data['followed_user_id'],
                        following_user_id    =   user_id
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
