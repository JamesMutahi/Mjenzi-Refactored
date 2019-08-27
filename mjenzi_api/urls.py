from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MaterialList, UserCreate, ReportList, CreateRequest

router = DefaultRouter()
router.register('projects', ProjectViewSet, base_name='projects')

urlpatterns = [
    path("projects/<int:pk>/reports/", ReportList.as_view(), name="reports_list"),
    path("projects/<int:pk>/materials/", MaterialList.as_view(), name="materials_list"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("projects/<int:pk>/materials/<int:choice_pk>/request/", CreateRequest.as_view(), name="create_request"),
]

urlpatterns += router.urls
