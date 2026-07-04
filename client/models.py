from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to="client_profiles/", blank=True, null=True)    
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
