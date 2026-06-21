from django.contrib.sitemaps import Sitemap

class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ['/', '/blog/']

    def location(self, item):
        return item