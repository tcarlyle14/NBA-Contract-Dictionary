import csv
import requests
from io import StringIO
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Player, GlobalSettings
from .forms import TeamForm, PlayerForm, GlobalSettingsForm

def team_list(request):
    teams = Team.objects.all()
    settings, created = GlobalSettings.objects.get_or_create(id=1, defaults={'salary_cap': 188931000})
    salary_cap = settings.salary_cap
    return render(request, 'nbaapp/team_list.html', {'teams': teams, 'salary_cap': salary_cap})
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'nbaapp/team_detail.html', {'team': team})
def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'nbaapp/player_detail.html', {'player': player})
def home(request):
    return render(request, 'nbaapp/home.html')
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'nbaapp/team_form.html', {'form': form})
def create_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            new_player = form.save()  # Save the form and get the instance of the new player
            return redirect('team_detail', team_id=new_player.team.id)  # Redirect to the team detail page
    else:
        form = PlayerForm()
    return render(request, 'nbaapp/player_form.html', {'form': form})
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm(instance=team)
    return render(request, 'nbaapp/team_form.html', {'form': form})
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'nbaapp/confirm_delete.html', {'team': team})
def edit_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('team_detail', team_id=player.team.id)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'nbaapp/player_form.html', {'form': form})
def delete_player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    team_id = player.team.id  # Capture the team ID to redirect after deletion
    if request.method == 'POST':
        player.delete()
        return redirect('team_detail', team_id=team_id)
    return render(request, 'nbaapp/confirm_delete_player.html', {'player': player})
def edit_salary_cap(request):
    settings, created = GlobalSettings.objects.get_or_create(id=1, defaults={'salary_cap': 188931000})
    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('team_list')  # Redirect back to the team list page after saving
    else:
        form = GlobalSettingsForm(instance=settings)
    return render(request, 'nbaapp/edit_salary_cap.html', {'form': form})

MICROSERVICE_URL = "http://127.0.0.1:8001/validate_csv/"  # default microser endpoint 

def upload_csv(request):
    if request.method == "POST":
        if 'file' not in request.FILES:
            return render(request, 'nbaapp/upload_csv.html', {"error": "No file uploaded."})

        csv_file = request.FILES['file']

        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return render(request, 'nbaapp/upload_csv.html', {"error": "Invalid file format. Please upload a CSV file."})

        try:
            # Send the file to the microservice for validation
            response = requests.post(
                MICROSERVICE_URL,
                files={'file': (csv_file.name, csv_file.read(), 'text/csv')}
            )

            # Process the microservice response
            if response.status_code != 200:
                error_message = response.json().get('error', 'An error occured with the microservice connection.')
                return render(request, 'nbaapp/upload_csv.html', {"error": error_message})
            
            # Validation succeeded: Process the file and save to database
            csv_file.seek(0)  # Reset file pointer for reading
            csv_data = StringIO(csv_file.read().decode('utf-8'))
            reader = csv.DictReader(csv_data)

            # Save data to the database
            for row in reader:
                try:
                    # Find or create if not already existing 
                    team, created = Team.objects.get_or_create(name=row['team'])

                    # Create a new player
                    Player.objects.create(
                        name=row['name'],
                        team=team,
                        salary=row['salary'],
                        position=row['position'],
                        college=row.get('college', ''),  # Optional field
                        years_experience=row['years_experience']
                    )
                except Exception as e:
                    print(f"Error saving row: {row} - {e}")

            return render(request, 'nbaapp/upload_csv.html', {"success": "File uploaded successfully!"})

        except requests.exceptions.RequestException as e:
            return render(request, 'nbaapp/upload_csv.html', {"error": f"Microservice error: {str(e)}"})

    # Handle GET request: Render the upload page
    return render(request, 'nbaapp/upload_csv.html')
