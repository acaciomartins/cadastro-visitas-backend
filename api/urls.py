from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VisitaViewSet, LojaViewSet, RitoViewSet,
    GrauViewSet, PotenciaViewSet, LoginView
)

router = DefaultRouter()
router.register(r'visitas', VisitaViewSet)
router.register(r'lojas', LojaViewSet)
router.register(r'ritos', RitoViewSet)
router.register(r'graus', GrauViewSet)
router.register(r'potencias', PotenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
] 