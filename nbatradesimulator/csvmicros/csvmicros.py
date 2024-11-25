import csv
from io import StringIO
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCEPTABLE_FIELDS = ['name', 'team', 'salary', 'position', 'college', 'years_experience']

@app.route('/validate_csv/', methods=['POST'])
def validate_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    csv_file = request.files['file']
    if not csv_file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

    try:
        # Read and validate the CSV content
        data = csv_file.read().decode('utf-8')
        csv_data = StringIO(data)
        reader = csv.DictReader(csv_data)

        # Validate columns
        if reader.fieldnames != ACCEPTABLE_FIELDS:
            return jsonify({"error": f"Invalid fields. Expected: {', '.join(ACCEPTABLE_FIELDS)}"}), 400

        # Validate rows
        errors = []
        for i, row in enumerate(reader, start=1):
            for field in ACCEPTABLE_FIELDS:
                if not row.get(field):
                    errors.append(f"Row {i}: Missing or empty field '{field}'")

            # Validate numeric fields
            try:
                salary = float(row.get('salary', 0))
                years_experience = int(row.get('years_experience', 0))
                if salary < 0 or years_experience < 0:
                    errors.append(f"Row {i}: Invalid values for salary or years_experience")
            except ValueError:
                errors.append(f"Row {i}: Salary and years_experience must be numeric")

        if errors:
            return jsonify({"error": "; ".join(errors)}), 400

        # If everything is valid, return success
        return jsonify({"message": "File validated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=8001, debug=True)  # default microservice runs on port 8002

