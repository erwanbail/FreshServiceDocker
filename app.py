from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "APIII ya rien a gratter igo"
DOMAIN = "DOMAIENE WEEE"
BASE_URL = f"https://{DOMAIN}.freshservice.com/api/v2/tickets"

def get_open_request_tickets():
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "per_page": 100,
        "page": 1,
        "filter": "new_and_my_open"
    }

    tickets_request_for = []

    while True:
        response = requests.get(BASE_URL, headers=headers, auth=(API_KEY, "X"), params=params)
        response.raise_for_status()
        data = response.json()

        tickets = data.get("tickets", [])
        if not tickets:
            break

        for ticket in tickets:
            subject = ticket.get("subject", "")
            status = ticket.get("status")
            if "request for" in subject.lower() and status == 2:
                tickets_request_for.append(ticket)

        params["page"] += 1

    return tickets_request_for

@app.route("/")
def index():
    return render_template("index.html", tickets=None)

@app.route("/fetch-tickets", methods=["POST"])
def fetch_tickets():
    tickets = get_open_request_tickets()
    return render_template("index.html", tickets=tickets)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
