from django.urls import path, include, re_path
from . import views
extrapatterns = [
    path('', views.Checkout,name="Checkout"),
    path('address/', views.ConfirmOrder,name="checkout"),
    path('<items_list>/', views.Checkout,name="Checkout"),
    path('address/success/<int:id>', views.OrderSuccess,name="OrderSuccess"),
    

]
urlpatterns = [
    path('', views.Home, name="Home"),
    path('login/', views.Login, name="login"),
    path('signup/', views.Signup, name="signup"),
    path('logout/', views.Logout, name="logout"),
    path('about/', views.About,name="AboutUs"),
    path('contact/', views.Contact,name="ContactUs"),
    path('tracker/', views.Tracker,name="TrackingStatus"),
    path('search/', views.Search,name="Search"),
    path('productview/<int:id>', views.ProductView,name="ProductView"),
   path('checkout/', include(extrapatterns))
]
