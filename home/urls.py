from django.urls import path
from django.conf import settings
from django.conf.urls.static import static,serve
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('recommend', views.recommend, name='recommend'),
    path('login', views.login_page, name='login'),
    path('person/<tab>', views.person_page, name='person'),
    path('anotherone/<int:id>/<tab>', views.anotherone_page, name='anotherone'),
    path('detail/<int:strategy_id>', views.detail_page, name='detail'),
    path('edit', views.edit_page, name='edit'),
    path('change', views.change, name='change'),
    path('logout', views.logout_page, name='logout'),
    path('register', views.register_page, name='register'),
    path('write', views.write_page, name='write'),
    path('like', views.like_strategy, name='like'),
    path('collection', views.collection_strategy, name='collection'),
    path('comment', views.comment, name='comment'),
    path('send_chat', views.send_chat, name='send_chat'),
    path('open_chat', views.open_chat, name='open_chat'),
    path('del_chat', views.del_chat, name='del_chat'),
    path('open_dialog/<int:id>', views.open_dialog, name='open_dialog'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('report', views.report, name='report'),
    path('search', views.search, name='search')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
