from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token


@csrf_exempt
def get_token(request):
    user, new = User.objects.get_or_create(username='admin')
    token, new = Token.objects.get_or_create(user=user)
    return JsonResponse({"token": token.key})
