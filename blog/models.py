from django.db import models
from django.urls import reverse
# from django.template.defaultfilters import slugify

from uuslug import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.CharField(max_length=30, editable=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def prev_article(self):
        return Article.objects.filter(id__gt=self.pk).order_by('id').first()

    def next_article(self):
        return Article.objects.filter(id__lt=self.pk).first()