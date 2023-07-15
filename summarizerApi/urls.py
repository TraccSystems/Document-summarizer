from django.urls import path,include
from . views import SummarizerTokenObtainPairView,SummarizerTokenRefreshView,SummarizerView
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
urlpatterns = [
    #path('auth/summarizer/token/', SummarizerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('auth/summarizer/token/refresh/',SummarizerTokenRefreshView.as_view(), name='token_refresh'),
    path('summarizer/<str:message>/<str:openai_api_key>/',SummarizerView.as_view(),name='Summarizer'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/summarizer/doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   
]