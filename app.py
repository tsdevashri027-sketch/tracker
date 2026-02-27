from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# path to data file where we keep history
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    # load existing entries so we can show history
    history = load_history()

    if request.method == 'POST':
        # read values from the form
        amount_str = request.form.get('amount', '0')
        reason = request.form.get('reason', '')

        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0

        # convert reason code to human text
        reason_map = {
            'personal': 'personal choice',
            'social': 'social obligation',
            'guilt': 'guilt or fear',
            'other': 'other'
        }
        reason_text = reason_map.get(reason, 'unknown')

        # calculate a simple independence score
        # higher for personal choices, lower for guilt or social pressure
        score_map = {
            'personal': 100,
            'social': 70,
            'guilt': 50,
            'other': 80
        }
        score = score_map.get(reason, 0)

        # advice based on score
        if score >= 90:
            advice = "Great independence! Keep trusting your choices."
        elif score >= 60:
            advice = "You're doing well, but watch for outside pressure."
        else:
            advice = "Try to pause and ask if this is really what you want."

        summary = {
            'amount': amount,
            'reason_text': reason_text,
            'score': score,
            'advice': advice
        }

        # add the new entry to history and save
        entry = {
            'amount': amount,
            'reason_text': reason_text,
            'score': score
        }
        history.append(entry)
        save_history(history)

        return render_template('index.html', summary=summary, history=history)

    # GET request: just show page with history
    return render_template('index.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
