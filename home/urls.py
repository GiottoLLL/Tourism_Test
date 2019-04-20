from django.urls import path
from django.conf import settings
from django.conf.urls.static import static,serve
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('person', views.person_page, name='person'),
    path('detail/<int:strategy_id>', views.detail_page, name='detail'),
    path('edit', views.edit_page, name='edit'),
    path('logout', views.logout_page, name='logout'),
    path('register', views.register_page, name='register'),
    path('write', views.write_page, name='write'),
    path('up_add/<int:strategy_id>', views.up_add, name='up_add'),
    path('like', views.like_strategy, name='like')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
