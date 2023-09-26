from django.urls import path,include
from . views import SummarizerView
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
urlpatterns = [
    #path('auth/summarizer/token/', SummarizerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('auth/summarizer/token/refresh/',SummarizerTokenRefreshView.as_view(), name='token_refresh'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('summarizer/',SummarizerView.as_view(),name='Summarizer'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  
]