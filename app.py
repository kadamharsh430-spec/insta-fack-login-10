
from flask import Flask, render_template, request
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Demo submissions
DATA_FILE = Path("submissions.txt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username", "").strip()
    game = request.form.get("game", "").strip()

    if not username or not game:
        return "Please fill both fields.", 400

    username = username[:50]
    game = game[:50]

    # Save demo data
    with DATA_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Username: {username}\n"
            f"Favorite Game: {game}\n"
            f"------------------------------\n"
        )

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Demo Submitted</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #fafafa;
                text-align: center;
                padding-top: 100px;
            }

            .box {
                background: white;
                display: inline-block;
                padding: 35px;
                border: 1px solid #ddd;
                border-radius: 12px;
            }

            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #0095f6;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>✅ Demo submitted</h2>
            <p>Your username and favorite game were saved.</p>
            <a href="/">Go back</a>
        </div>
    </body>
    </html>
    """


@app.route("/entries")
def entries():
    submissions = []

    if DATA_FILE.exists():
        text = DATA_FILE.read_text(encoding="utf-8").strip()

        if text:
            blocks = text.split("------------------------------")

            for block in blocks:
                block = block.strip()

                if not block:
                    continue

                entry = {}

                for line in block.splitlines():
                    if line.startswith("Time:"):
                        entry["time"] = line.replace("Time:", "", 1).strip()

                    elif line.startswith("Username:"):
                        entry["username"] = line.replace(
                            "Username:", "", 1
                        ).strip()

                    elif line.startswith("Favorite Game:"):
                        entry["game"] = line.replace(
                            "Favorite Game:", "", 1
                        ).strip()

                submissions.append(entry)

    return render_template(
        "entries.html",
        submissions=submissions
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

