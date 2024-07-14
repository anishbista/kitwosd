from django.db import models
from django.utils.text import slugify, _
from tinymce import models as tmcemodel


from utils.common import CommonModel


class BlogPage(CommonModel):
    title = models.CharField(max_length=500, null=False, blank=False)
    sub_title = models.TextField()


class Blog(CommonModel):
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    short_description = models.TextField(
        default="", max_length=100, null=False, blank=False
    )

    description = tmcemodel.HTMLField(null=False, blank=False)
    tags = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
    )
    priority = models.PositiveIntegerField(default=0)
    publish = models.BooleanField(default=True)

    class Meta:
        ordering = ("-priority",)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title[:40])
            while Blog.objects.filter(slug=slug).exists():
                slug = slugify(self.title[:20] + str(self.pk)[:20])
            self.slug = slug
        return super().save(*args, **kwargs)


class BlogImage(CommonModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="images")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog/items/")
    alt = models.CharField(max_length=255, null=True, blank=True)
    priority = models.PositiveIntegerField(default=0)
    publish = models.BooleanField(default=True)

    class Meta:
        ordering = ("-priority",)
