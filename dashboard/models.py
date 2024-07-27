from django.db import models


class Dashboard(models.Model):
    """Dashboard model"""

    new_users = models.IntegerField()
    new_enterprises = models.IntegerField()
    new_self_employed = models.IntegerField()
    
    

    def __str__(self):
        return self.name
