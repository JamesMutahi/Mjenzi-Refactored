from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html')


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by("-date_posted")
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        a_project = Project.objects.create(
            project_name=request.data["project_name"],
            contractor_email=request.data["contractor_email"],
            description=request.data["description"],
            user=request.user,
            developer_email=request.user.email
        )
        email = request.data["contractor_email"]
        send_mail(
            'MJENZI',
            'Hello,'
            'A developer has created a project with your name on it. Register and login to view project details'
            'Cheers!'
            'Innovex.',
            ['{email}'.format(email=email)],
            fail_silently=True,
        )
        return Response(
            data=ProjectSerializer(a_project).data,
            status=status.HTTP_201_CREATED
        )

    def get_queryset(self):
        users = Project.objects.filter(user=self.request.user)
        emails = Project.objects.filter(contractor_email=self.request.user.email)
        return Project.objects.filter(id__in=users or emails)


class ProjectDetail(generics.RetrieveDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.user:
            raise PermissionDenied("You can not delete this project.")
        return super().destroy(request, *args, **kwargs)


class MaterialList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Materials.objects.filter(project_id=self.kwargs["pk"])
        return queryset

    serializer_class = MaterialsSerializer


class ReportList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Reports.objects.filter(project_id=self.kwargs["pk"]).order_by("-date_posted")
        return queryset

    serializer_class = ReportSerializer


class RequestList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Requests.objects.filter(project_id=self.kwargs["pk"]).order_by("-date_posted")
        return queryset

    serializer_class = RequestSerializer

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs["pk"])
        if not request.user == project.user:
            raise PermissionDenied("You can not create requests for this project.")
        return super().post(request, *args, **kwargs)


class RequestDetail(generics.RetrieveDestroyAPIView):
    queryset = Requests.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RequestSerializer

    def put(self, request, *args, **kwargs):
        try:
            a_request = self.queryset.get(pk=kwargs["pk"])
            serializer = RequestSerializer()
            updated_request = serializer.update(a_request, request.data)
            return Response(RequestSerializer(updated_request).data)
        except ObjectDoesNotExist:
            return Response(
                data={
                    "message": "Request with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    """
    POST auth/register/
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        password2 = request.data.get("password2", "")
        email = request.data.get("email", "")
        if not username and not password and not email and not password2:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if password != password2:
            return Response(
                data={
                    "message": "Passwords don't match"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        Token.objects.create(user=new_user)
        send_mail(
            'MJENZI',
            'Congratulations you have been succesfully registered. Welcome to Mjenzi App.',
            'cheers!, '
            'Innovex.'
            "{EMAIL_HOST_USER}",
            ['{email}'.format(email=email)],
            fail_silently=True,
        )
        return Response(
            data=UserSerializer(new_user).data, status=status.HTTP_201_CREATED
        )


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
