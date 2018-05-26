from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.utils import slugify
from django.contrib.auth.models import User
from django.shortcuts import resolve_url


# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    body = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def point_count(self):
        return self.point_set.count()

    @property
    def points(self):
        return self.point_set

    @property
    def comments(self):
        return self.comment_set

    @property
    def comment_count(self):
        return self.comment_set.count()

    @property
    def is_link(self):
        return self.url

    def get_absolute_url(self):
        return resolve_url('topics_detail', slug=self.slug)

    def get_topic_url(self):
        if self.is_link:
            return self.url

        return self.get_absolute_url()

    def is_voted_by_user(self, user_id):
        return self.points.filter(user_id=user_id).exists()


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


@receiver(post_save, sender=Topic)
def unique_slug_for_topic(sender, **kwargs):
    topic = kwargs['instance']

    if not topic.slug:
        slug = slugify(topic.title)

        if Topic.objects.filter(slug=slug).exists():
            slug += "-" + str(topic.id)

        topic.slug = slug
        topic.save()
