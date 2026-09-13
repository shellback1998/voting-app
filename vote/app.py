from flask import Flask, render_template_string, request
import redis

app = Flask(__name__)

# Connect to Redis using the Docker Compose service name "redis"
r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Turing Pi Voting App</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, Helvetica, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #f8fafc;
        }

        .card {
            width: 90%;
            max-width: 520px;
            padding: 40px;
            border-radius: 18px;
            background: #ffffff;
            color: #1e293b;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        }

        h1 {
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 2rem;
        }

        .subtitle {
            margin-bottom: 30px;
            color: #64748b;
            font-size: 1.05rem;
        }

        .buttons {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }

        button {
            min-width: 150px;
            padding: 16px 24px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
        }

        .cats {
            background: #2563eb;
            color: white;
        }

        .dogs {
            background: #16a34a;
            color: white;
        }

        .message {
            margin-top: 28px;
            padding: 14px;
            border-radius: 10px;
            background: #f1f5f9;
            font-size: 1.05rem;
        }

        .footer {
            margin-top: 25px;
            font-size: 0.85rem;
            color: #94a3b8;
        }
    </style>
</head>

<body>

    <div class="card">

        <h1>Turing Pi Voting App</h1>

        <p class="subtitle">
            Vote for your favorite
        </p>

        <form method="POST">

            <div class="buttons">

                <button
                    class="cats"
                    type="submit"
                    name="vote"
                    value="Cats">
                    Cats
                </button>

                <button
                    class="dogs"
                    type="submit"
                    name="vote"
                    value="Dogs">
                    Dogs
                </button>

            </div>

        </form>

        {% if vote %}
            <div class="message">
                You voted for:
                <strong>{{ vote }}</strong>
            </div>
        {% endif %}

        <div class="footer">
            Powered by Flask, Redis, PostgreSQL and Docker Compose
        </div>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():

    vote = None

    if request.method == "POST":

        vote = request.form.get("vote")

        if vote:
            # Add the vote to the Redis list called "votes"
            r.rpush("votes", vote)

    return render_template_string(
        PAGE,
        vote=vote
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )