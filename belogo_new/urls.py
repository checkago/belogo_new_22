from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('email-signals/', include('email_signals.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
]

# if settings.MEDIA_ROOT:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += staticfiles_urlpatterns()


handler404 = "web.views.page_not_found_view"
