from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():

    data = request.get_json()
    text = data["text"].lower()
    type_ = data["type"]

    score = 0
    reason = ""

    # SPAM CHECK
    if type_ == "Spam":
        if "free" in text:
            score += 1
            reason += "Contains word 'free'\n"
        if "win" in text:
            score += 1
            reason += "Contains word 'win'\n"
        if "money" in text:
            score += 1
            reason += "Mentions money\n"
        if "urgent" in text:
            score += 1
            reason += "Uses urgency\n"

    # PHISHING CHECK
    elif type_ == "Phishing":
        if "password" in text:
            score += 1
            reason += "Mentions password\n"
        if "bank" in text:
            score += 1
            reason += "Mentions bank\n"
        if "verify" in text:
            score += 1
            reason += "Asks for verification\n"

    # FAKE NEWS CHECK
    elif type_ == "Fake News":
        if "breaking" in text:
            score += 1
            reason += "Uses breaking news\n"
        if "shocking" in text:
            score += 1
            reason += "Clickbait word\n"
        if "unbelievable" in text:
            score += 1
            reason += "Exaggeration detected\n"

    # RESULT
    if score >= 3:
        result = "High Risk ⚠️"
        level = "high"
    elif score == 2:
        result = "Medium Risk ⚠️"
        level = "medium"
    else:
        result = "Low Risk ✅"
        level = "low"

    return jsonify({
        "result": result,
        "reason": reason,
        "level": level
    })


if __name__ == "__main__":
    app.run(debug=True)