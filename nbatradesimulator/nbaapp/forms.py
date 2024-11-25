from django import forms
from .models import Team, Player, GlobalSettings
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'team', 'salary', 'position', 'college', 'years_experience']
class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['salary_cap']
class TradeForm(forms.Form):
    player_from_team_a = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        label="Player from Team A"
    )
    player_from_team_b = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        label="Player from Team B"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the label for each player
        self.fields['player_from_team_a'].label_from_instance = self.get_player_label
        self.fields['player_from_team_b'].label_from_instance = self.get_player_label
    def get_player_label(self, player):
        return f"{player.name} ({player.team.name})"