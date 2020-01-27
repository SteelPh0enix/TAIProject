from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add_spectrogram/', views.add_spectrogram, name='add_spectrogram'),
    path('spectrogram/<int:id>/toggle_fav', views.spectrogram_toggle_fav, name='toggle_spectrogram_favourite'),
    path('spectrogram/<int:id>/votes', views.get_spectrogram_votes, name='get_spectrogram_votes'),
    path('spectrogram/<int:id>/edit', views.edit_spectrogram, name='edit_spectrogram'),
    path('spectrogram/<int:id>/delete', views.delete_spectrogram, name='delete_spectrogram'),
    path('user', views.view_user_profile, name='view_user_profile'),
    path('spectrogram/edit', views.edit_spectrogram_json, name='edit_spectrogram_json'),
    path('top', views.top_spectrums, name="top_spectrums"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
