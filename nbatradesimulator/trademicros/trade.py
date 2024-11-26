import os
import sys
import django
from decimal import Decimal  # Import Decimal
# Add the project directory to the Python path
sys.path.append('/Users/trevorcarlyle/Desktop/NBA-Contract-Dictionary/nbatradesimulator')
# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbatradesimulator.settings')
# Setup Django
django.setup()
from nbaapp.models import Team, GlobalSettings
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/validate_trade/', methods=['POST'])
def validate_trade():
    data = request.json
    team_a_id = data['team_a_id']
    team_b_id = data['team_b_id']
    player_a_salary = Decimal(data['player_a_salary'])  # Convert to Decimal
    player_b_salary = Decimal(data['player_b_salary'])  # Convert to Decimal
    try:
        team_a = Team.objects.get(id=team_a_id)
        team_b = Team.objects.get(id=team_b_id)
        salary_cap = GlobalSettings.objects.get(id=1).salary_cap
        # Ensure salary_cap is also a Decimal
        salary_cap = Decimal(salary_cap)
        new_team_a_payroll = team_a.payroll - player_a_salary + player_b_salary
        new_team_b_payroll = team_b.payroll - player_b_salary + player_a_salary
        if new_team_a_payroll > salary_cap or new_team_b_payroll > salary_cap:
            return jsonify({'valid': False, 'error': 'Trade Failed: Trade would exceed salary cap.'})
        else:
            return jsonify({'valid': True, 'message': 'Trade is valid and successful!'})
    except Team.DoesNotExist:
        return jsonify({'valid': False, 'error': 'One or both teams not found.'})
    except GlobalSettings.DoesNotExist:
        return jsonify({'valid': False, 'error': 'Global settings not found.'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)