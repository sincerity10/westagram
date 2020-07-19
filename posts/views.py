import json
import jwt

from django.http    import JsonResponse
from django.views   import View

from posts.models   import Post,Comment,Like
from users.models   import User
from my_settings    import SECRET_KEY
from utils          import login_decorator

class PostRegister(View):

    @login_decorator
    def post(self,request):
        data    =   json.loads(request.body)
        user_id =   request.user.id

        try:
            if data['post_text'] and data['image_url']:

                if User.objects.filter(id=user_id).exists():
                    Post(
                        post_text   =   data['post_text'],
                        image_url   =   data['image_url'],
                        user_id     =   user_id
                    ).save()
                    return JsonResponse({'message':'Post Register Success'}, status=200)

                return JsonResponse({'message':'INVALID_User_id'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class CommentRegister(View):

    @login_decorator
    def post(self,request):
        data    =   json.loads(request.body)

        try:
            if data['comment_text'] and data['post_id']:

                if Post.objects.filter(id=data['post_id']).exists():
                    Comment(
                        comment_text    =   data['comment_text'],
                        post_id         =   data['post_id'],
                        comment_user_id =   request.user.id
                    ).save()
                    comment_list    =   []
                    comments        =   Comment.objects.filter(post_id=data['post_id'])
                    for comment in comments:
                        comment_list.append({'num':comment.id,'comment_text':comment.comment_text})
                    print(comment_list)
                    return JsonResponse({'comments':comment_list}, status=200)

                return JsonResponse({'message':'INVALID_Post_id'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class PostLike(View):

    @login_decorator
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['post_id']:

                if Post.objects.filter(id=data['post_id']).exists():
                    user_id =   request.user.id

                    if Like.objects.filter(post_id=data['post_id'],user_id=user_id).exists():
                        target_post         =   Post.objects.get(id=data['post_id'])
                        target_post.likes  -=   1
                        target_post.save()
                        like_obj            =   Like.objects.filter(post_id=data['post_id'],user_id=request.user.id)
                        like_obj.delete()
                        return JsonResponse({'message':f"Unlike post id:{data['post_id']}"}, status=200)

                    target_post         =   Post.objects.get(id=data['post_id'])
                    target_post.likes   +=  1
                    target_post.save()
                    like_obj            =   Like(post_id=data['post_id'],user_id=request.user.id)
                    like_obj.save()

                    return JsonResponse({'message':f"Like post id:{data['post_id']}"}, status=200)

                return JsonResponse({'message':'INVALID_Post_id'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
