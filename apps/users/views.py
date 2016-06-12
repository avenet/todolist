from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer


class UserCreate(APIView):
    """
    Creates a new user.
    """
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = serializer.instance
            user.set_password(request.data['password'])
            user.save(update_fields=['password'])

            return Response({},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
