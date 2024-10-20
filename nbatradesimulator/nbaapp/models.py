from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    @property
    def payroll(self):
        return sum(player.salary for player in self.players.all())
    @property
    def is_over_cap(self):
        try:
            settings = GlobalSettings.objects.get(id=1)  # Assuming there's a single instance
            if self.payroll > settings.salary_cap:
                return 'Yes'
            else:
                return 'No'
        except GlobalSettings.DoesNotExist:
            return None
    @property
    def payroll_available(self):
        settings = GlobalSettings.objects.get(id=1)
        return settings.salary_cap - self.payroll

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=50)
    college = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField()
    def __str__(self):
        return self.name
    
class GlobalSettings(models.Model):
    salary_cap = models.DecimalField(max_digits=12, decimal_places=2, default=188931000)
    def __str__(self):
        return "Global Settings"
    class Meta:
        verbose_name_plural = "Global Settings"
