"""versescanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .views import pages
from .views.json import batch, index, manage

admin.autodiscover()

urlpatterns = [
    path('', pages.index_page),
    path('robots\.txt', pages.robots),
    path('batch/', pages.batch_page),
    path('help/', pages.help_page),
    path('about/', pages.about_page),
    path('login/', pages.login_page),
    path('logout/', pages.logout_page),
    path('register/', pages.register_page),
    path('profile/', pages.profile_page),
    path('manage/', pages.manage_page),
    path('admin/', admin.site.urls),
    path('json/poem/<int:key>', index.get_poem_length),
    path('json/<slug:obj_type>/<int:key>', index.get_list_type),  # author, opus, book
    path('json/authors/', index.get_authors),
    path('json/verse/<int:poem>/<int:verse>', index.get_verse),
    path('json/verse/random/', index.get_random_verse),
    path('json/verse/forms/', index.get_verse_forms),
    path('json/scan/dbverse/<int:poem>/<int:verse>', index.scan_verse),
    path('json/scan/text/<str:txt>', index.scan_verse_text),
    path('json/batch/clearcurrentsession', batch.clear_batch_session),
    path('json/batch/save', batch.save_batch),
    path('json/batch/delete/<int:batchid>', batch.delete_batch),
    path('json/batch/run/<int:batchid>', batch.run_batch),
    path('json/batch/deleteverse/<slug:hashvalue>', batch.delete_verse_hash),
    path('json/batches/', batch.get_batches),
    path('json/batchitem/save/', batch.save_batchitems),
    path('json/admin/sync/files/', manage.sync_files),
    path('json/admin/sync/db/', manage.sync_db),
    path('json/admin/users/', manage.get_member_list),
    path('json/admin/meta/', manage.post_meta),
    path('blog/', include('zinnia.urls')),
    path('comments/', include('django_comments.urls')),
]
