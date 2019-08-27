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
            raise PermissionDenied("You can not create materials for this project.")
        return super().post(request, *args, **kwargs)


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


class CreateRequest(APIView):
    serializer_class = RequestSerializer

    def post(self, request, pk, material_pk):
        requested_by = request.data.get("requested_by")
        data = {'Material': material_pk, 'project': pk, 'requested_by': requested_by}
        serializer = RequestSerializer(data=data)
        if serializer.is_valid():
            request = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
