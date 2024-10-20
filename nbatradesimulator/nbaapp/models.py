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
        if self.payroll > settings.NBA_SALARY_CAP:
            return True
        else:
            return False

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=50)
    college = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField()
    def __str__(self):
        return self.name
