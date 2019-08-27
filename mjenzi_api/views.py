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

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.created_by:
            raise PermissionDenied("You can not delete this project.")
        return super().destroy(request, *args, **kwargs)


class MaterialList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Materials.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = MaterialsSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


