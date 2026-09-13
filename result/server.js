const express = require("express");
const { Pool } = require("pg");

const app = express();

const pool = new Pool({
    host: "db",
    database: "votes",
    user: "postgres",
    password: "postgres",
    port: 5432
});

app.get("/", async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT vote, COUNT(*) AS count
            FROM votes
            GROUP BY vote
            ORDER BY vote
        `);

        let totalVotes = 0;

        for (const row of result.rows) {
            totalVotes += parseInt(row.count);
        }

        let resultCards = "";

        for (const row of result.rows) {
            const count = parseInt(row.count);

            const percentage =
                totalVotes > 0
                    ? Math.round((count / totalVotes) * 100)
                    : 0;

            resultCards += `
                <div class="result-card">
                    <div class="result-header">
                        <span class="choice">${row.vote}</span>
                        <span class="count">${count} votes</span>
                    </div>

                    <div class="progress">
                        <div
                            class="progress-bar"
                            style="width: ${percentage}%">
                        </div>
                    </div>

                    <div class="percentage">
                        ${percentage}%
                    </div>
                </div>
            `;
        }

        const html = `
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Turing Pi Voting Results</title>

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

            background:
                linear-gradient(
                    135deg,
                    #0f172a,
                    #1e293b
                );
        }

        .container {
            width: 90%;
            max-width: 650px;
        }

        .main-card {
            background: white;

            padding: 40px;

            border-radius: 18px;

            box-shadow:
                0 20px 50px
                rgba(0, 0, 0, 0.30);
        }

        h1 {
            margin-top: 0;

            text-align: center;

            color: #1e293b;

            font-size: 2rem;
        }

        .summary {
            text-align: center;

            color: #64748b;

            margin-bottom: 30px;

            font-size: 1.05rem;
        }

        .result-card {
            background: #f8fafc;

            padding: 20px;

            margin-bottom: 18px;

            border-radius: 12px;
        }

        .result-header {
            display: flex;

            justify-content: space-between;

            margin-bottom: 12px;
        }

        .choice {
            font-size: 1.2rem;

            font-weight: bold;

            color: #1e293b;
        }

        .count {
            color: #64748b;
        }

        .progress {
            height: 14px;

            overflow: hidden;

            border-radius: 999px;

            background: #e2e8f0;
        }

        .progress-bar {
            height: 100%;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #22c55e
                );
        }

        .percentage {
            margin-top: 8px;

            text-align: right;

            font-weight: bold;

            color: #1e293b;
        }

        .footer {
            margin-top: 25px;

            text-align: center;

            font-size: 0.85rem;

            color: #94a3b8;
        }
    </style>
</head>

<body>

    <div class="container">

        <div class="main-card">

            <h1>Turing Pi Voting Results</h1>

            <div class="summary">
                Total votes: ${totalVotes}
            </div>

            ${resultCards}

            <div class="footer">
                Powered by Node.js, PostgreSQL and Docker Compose
            </div>

        </div>

    </div>

</body>

</html>
        `;

        res.send(html);

    } catch (error) {

        console.error(error);

        res.status(500).send(
            "Database error"
        );
    }
});


app.listen(
    3000,
    "0.0.0.0",
    () => {
        console.log(
            "Result app running on port 3000"
        );
    }
);