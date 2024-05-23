# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from main import calculate_loan  # Import the calculate_loan function

app = Flask(__name__, static_folder="build", static_url_path="")
CORS(app)  # Enable CORS for all routes


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    initial_interest_rate = float(data.get("initialInterestRate"))
    loan_amount = float(data.get("loanAmount"))
    repayment_period_years = int(data.get("repaymentPeriodYears"))
    salaries = data.get("salaries")
    splits = data.get("splits")
    names = data.get("names")

    result = calculate_loan(
        initial_interest_rate,
        loan_amount,
        repayment_period_years,
        salaries,
        splits,
        names,
    )
    return jsonify(result)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
