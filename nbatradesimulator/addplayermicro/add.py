import os
import sys
import django
from decimal import Decimal
from flask import Flask, request, jsonify
# Add the project directory to the Python path
sys.path.append('/Users/trevorcarlyle/Desktop/NBA-Contract-Dictionary/nbatradesimulator')
# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nbatradesimulator.settings')
# Setup Django
django.setup()
from nbaapp.models import Team, GlobalSettings
app = Flask(__name__)
@app.route('/verify_salary/', methods=['POST'])
def verify_salary():
    data = request.json
    team_id = data.get('team_id')
    new_player_salary = Decimal(data.get('new_player_salary'))
    try:
        team = Team.objects.get(id=team_id)
        available_payroll = team.payroll_available
        if new_player_salary > available_payroll:
            return jsonify({
                'valid': False,
                'error': (
                    f"Error: New player salary exceeds available payroll. "
                    f"Available payroll is ${available_payroll:.2f}. "
                    "To add a player to this team, please lower the salary."
                )
            })
        else:
            return jsonify({'valid': True, 'message': 'New player salary fits within available payroll.'})
    except Team.DoesNotExist:
        return jsonify({'valid': False, 'error': 'Team not found.'}), 404
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)