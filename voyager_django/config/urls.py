# voyager_django URL Configuration

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseBadRequest
from django.template import loader

urlpatterns = [
    path("admin/", admin.site.urls),
    path("procedure_writer/", include('procedure_writer.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





# need custom error handling since Django default views don't correctly render the error message
def response_error_handler_400(request, exception=None):
    template = loader.get_template('400.html')
    return HttpResponseBadRequest(template.render(request=request, context={'exception': str(exception)}))

handler400 = response_error_handler_400
