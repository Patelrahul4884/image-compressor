from django.db import models


class Token(models.Model):
    token = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.token


class Upload(models.Model):
    image = models.ImageField(upload_to='', blank=False, null=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, default='')

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Upload, self).delete(*args, **kwargs)
