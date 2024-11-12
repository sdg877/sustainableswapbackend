from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_title = models.CharField(max_length=30)
    item_description = models.CharField(max_length=100)
    listing_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.FileField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.item_title}'
    
class Swap(models.Model):
    item_title = models.CharField(max_length=30)
    item_description = models.CharField(max_length=100)
    offer_accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s offer for {self.item.item_title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for item_id: {self.item_id} @{self.url}"
