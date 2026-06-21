from django.contrib.sitemaps import Sitemap

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['', '/blog/']

    def location(self, item):
        return item