from django.urls import path
from django.conf import settings
from django.conf.urls.static import static,serve
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('person', views.person_page, name='person'),
    path('detail', views.detail_page, name='detail'),
    path('edit', views.edit_page, name='edit'),
    path('logout', views.logout_page, name='logout'),
    path('register', views.register_page, name='register'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
