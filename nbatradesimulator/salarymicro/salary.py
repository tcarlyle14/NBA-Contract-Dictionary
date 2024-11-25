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
from nbaapp.models import Player
app = Flask(__name__)
# Example conversion rate from USD to EUR
USD_TO_EUR_RATE = Decimal('0.95')  # This is a placeholder; you might want to fetch real-time rates
@app.route('/convert_salary/', methods=['POST'])
def convert_salary():
    data = request.json
    player_id = data.get('player_id')
    try:
        player = Player.objects.get(id=player_id)
        salary_usd = player.salary
        salary_eur = salary_usd * USD_TO_EUR_RATE
        return jsonify({
            'player_name': player.name,
            'salary_usd': float(salary_usd),
            'salary_eur': float(salary_eur),
            'message': f"The salary of {player.name} is ${salary_usd} USD, which is approximately €{salary_eur:.2f} EUR."
        })
    except Player.DoesNotExist:
        return jsonify({'error': 'Player not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)