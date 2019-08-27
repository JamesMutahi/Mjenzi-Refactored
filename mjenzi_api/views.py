from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from .models import *
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MaterialList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Materials.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = MaterialsSerializer


class ReportList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Reports.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.created_by:
            raise PermissionDenied("You can not create reports for this project.")
        return super().post(request, *args, **kwargs)


class RequestList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Requests.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = RequestSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
