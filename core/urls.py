# # Cattel-breed/urls.py

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from portal import views as portal_views

# urlpatterns = [
#     path('admin-django/', admin.site.urls), # Standard Django Admin
#     path('admin/', admin.site.urls),

#     # Landing & Core Pages
#     path('', portal_views.landing_view, name='landing'),

#     # Project Apps
#     # path('', include('core.urls')),              # Landing & Public pages
#     path('accounts/', include('accounts.urls')), # Signup, Login, SMTP verify
#     path('dashboard/', include('portal.urls')),  # Main User Hub
#     # path('ai/', include('recognition.urls')),    # Gemini AI processing
#     path('breeds/', include('breeds.urls')),     # Breed information library
#     path('history/', include('history.urls')),   # Past scan logs
#     path('reports/', include('reports.urls')),   # Charts & PDF generation
#     path('notifications/', include('notifications.urls')), 
#     path('profile/', include('profiles.urls')),
#     # path('admin-panel/', include('adminpanel.urls')), # Custom Admin Dashboard
#     # path('chatbot/', include('chatbot.urls')),
#     path('portal/', include('portal.urls')), # Main User Hub
# ]

# # Serving media files (for cattle images) during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portal.views import landing_view # Import it directly

urlpatterns = [
    path('', landing_view, name='landing'), # Global name 'landing'
    path('admin/', admin.site.urls),
    path('', include('portal.urls')), # This handles landing/dashboard
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('history/', include('history.urls')),
    path('notifications/', include('notifications.urls')),
    path('breeds/', include('breeds.urls')),
    path('reports/', include('reports.urls')),
    path('admin-django/', admin.site.urls),
    path('recognition/', include('recognition.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)