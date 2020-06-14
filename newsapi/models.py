from django.db import models

class NewsSource(models.Model):

    name = models.CharField(max_length = 20, blank = True, null = True)
    short_name = models.CharField(max_length = 5, blank = True, null = True, unique = True)
    last_updated = models.DateTimeField(blank = True, null = True)

    def __str__(self):

        return(f'Source:{self.short_name}_{self.last_updated}')


class Article(models.Model):

    news_source = models.ForeignKey(NewsSource, on_delete = models.CASCADE)
    link = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):

        return(f'Article:{self.news_source}_{self.link}')
