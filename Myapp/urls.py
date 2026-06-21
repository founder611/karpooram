from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from Myapp.sitemaps import StaticSitemap
from Myapp import views

sitemaps = {
    'static': StaticSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.homepage),
    path('order_post/', views.order_post),
    path('raz_pay/<amount>', views.raz_pay),
    path('userpayment_post/', views.userpayment_post),
    path('emailenquiry/', views.emailenquiry),
    path('blog/', views.blog_page),
    path(
        "googleca06e218bc89f31c.html",
        TemplateView.as_view(
            template_name="googleca06e218bc89f31c.html",
            content_type="text/html"
        ),
    ),
    path(
    'sitemap.xml',
    sitemap,
    {'sitemaps': sitemaps},
    name='sitemap'
),
]