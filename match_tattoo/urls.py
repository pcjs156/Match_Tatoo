from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import mainApp.urls
import accountApp.urls
import matchingApp.urls
import tattooistApp.urls

# 다른 app으로부터 include되는 url
included_urls = [
    path('', include(mainApp.urls)),
    path('account/', include(accountApp.urls)),
    path('matching/', include(matchingApp.urls)),
    path('tattooist/', include(tattooistApp.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
] + included_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
