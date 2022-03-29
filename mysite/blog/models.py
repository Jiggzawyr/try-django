from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.db.models import Q


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (Q(title__icontains=query)
                  | Q(content__icontains=query)
                  | Q(slug__icontains=query)
                  | Q(user__first_name__icontains=query)
                  | Q(user__last_name__icontains=query)
                  | Q(user__email__icontains=query)
                  )
        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class BlogPost(models.Model):
    user = models.ForeignKey(get_user_model(), default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = BlogPostManager()

    class Meta:
        ordering: ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/blog/detail/{self.slug}"

    def get_edit_url(self):
        return f"/blog/update/{self.slug}"

    def get_delete_url(self):
        return f"/blog/delete/{self.slug}"
