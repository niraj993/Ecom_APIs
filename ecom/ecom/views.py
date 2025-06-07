from django.http import HttpRequest,JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from configs.response_messages import SERVER_IS_LIVE
from configs.constaints import STATUS_CODE,STATUS_CODE,MESSAGE,GET_METHOD



@api_view([GET_METHOD])
def index(request:HttpRequest)->Response:
    return Response({STATUS_CODE:200,MESSAGE:SERVER_IS_LIVE})

