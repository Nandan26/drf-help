from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name = 'product-detail'),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name = 'product-update'),
    path('<int:pk>/delete/', views.ProductDestroyAPIView.as_view()),
    path('', views.ProductListCreateAPIView.as_view(), name = 'product-list'),
    
    # path('', views.ProductMixinView.as_view()),
    # path('', views.product_alt_view)
    # path('<int:pk>/', views.product_alt_view)
]