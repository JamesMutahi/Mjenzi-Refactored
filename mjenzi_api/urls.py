from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, base_name='projects')

urlpatterns = [

]

urlpatterns += router.urls