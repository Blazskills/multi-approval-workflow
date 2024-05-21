from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from django.contrib.auth import authenticate

from account.tokens import create_jwt_pair_for_user
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions

from utils.decorators import DisallowedUserPermission


class testaccount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "status": "Account okay",
            "code": 200,
        }
        return Response(data)







class LoginView(APIView):
    authentication_classes = []

    @swagger_auto_schema(
        operation_id='login',
        operation_description='Login',
        request_headers={
            'Content-Type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The content type of the request',
                required=['request_headers']
            )
        },

        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="user@gmail.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="**********")
            }
        ),
        responses={
            200: openapi.Response(
                description='Login success',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Login successful.")
                    }
                )
            ),
            400: openapi.Response(
                description='Invalid request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='All 400 errors'),
                    }
                )
            )
        },
        tags=['account']
    )
    def post(self, request):
        def create_response(status, message, status_code):
            response = {"status": status, "message": message}
            return Response(data=response, status=status_code)

        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password", "")
        if not email or not password:
            return Response(
                {"error": "Email and Password cannot be empty", "message": "Bad Request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
        except:
            return Response(
                {"status": "error", "status_message": "Bad Request", "message": "User not found", },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = authenticate(username=user.username, password=password)
            if not user:
                raise AuthenticationFailed("Invalid email or password")
            if user.user_type not in ["vc", "dvc", "registrar", "dean",
                                      "hod", "lecturer"]:
                return create_response(
                    "error", "Oops, You are not allowed.", status.HTTP_400_BAD_REQUEST
                )
            elif not user.is_verified:
                return create_response(
                    "error", "Account not verified", status.HTTP_400_BAD_REQUEST
                )
            elif user.is_blocked:
                return create_response(
                    "error", "Account blocked", status.HTTP_400_BAD_REQUEST
                )
            elif not user.is_active:
                return create_response(
                    "error", "Account not active", status.HTTP_400_BAD_REQUEST
                )
            elif user.is_deleted:
                return create_response(
                    "error", "Account deleted", status.HTTP_400_BAD_REQUEST
                )
            tokens = create_jwt_pair_for_user(user)
            # deleting temporary password the first time user is login
            user.temp_password = ""
            user.save()
            response = {
                "message": "Login successful",
                "ut": user.user_type,
                "token": tokens,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except (ValidationError, ObjectDoesNotExist, AuthenticationFailed) as e:
            print(f'An exception occurred: {e}')
            data = {"status": 'error', "message": str(e)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST,)

