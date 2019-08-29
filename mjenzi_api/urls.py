from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MaterialList, UserCreate, ReportList, RequestList, LoginView

router = DefaultRouter()
router.register('projects', ProjectViewSet, base_name='projects')

urlpatterns = [
    path("projects/<int:pk>/reports/", ReportList.as_view(), name="reports_list"),
    path("projects/<int:pk>/materials/", MaterialList.as_view(), name="materials_list"),
    path("projects/<int:pk>/requests/", RequestList.as_view(), name="create_request"),
    path("sign-up/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls
