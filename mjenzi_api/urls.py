from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, MaterialList

router = DefaultRouter()
router.register('projects', ProjectViewSet, base_name='projects')

urlpatterns = [
    path("projects/<int:pk>/materials/", MaterialList.as_view(), name="materials_list"),
]

urlpatterns += router.urls
