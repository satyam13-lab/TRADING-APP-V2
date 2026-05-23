import sys
from pathlib import Path

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

sys.path.append(str(ROOT_DIR))

from flask import Flask, request

from broker.zerodha.auth import (
    ZerodhaAuth
)


app = Flask(__name__)

auth = ZerodhaAuth()


@app.route("/")
def home():

    try:

        print(
            "\n========== CALLBACK RECEIVED =========="
        )

        request_token = request.args.get(
            "request_token"
        )

        print(
            f"\nREQUEST TOKEN:\n{request_token}"
        )

        if not request_token:

            return """
            <h2>
            Request token missing
            </h2>
            """

        response = auth.generate_session(
            request_token
        )

        print(
            "\n========== SESSION RESPONSE =========="
        )

        print(response)

        if response.get("status"):

            return """
            <html>

            <head>

                <title>
                    Zerodha Connected
                </title>

                <style>

                    body {

                        background: #F5F9FF;

                        display: flex;

                        justify-content: center;

                        align-items: center;

                        height: 100vh;

                        font-family: Arial;
                    }

                    .card {

                        background: white;

                        padding: 50px;

                        border-radius: 20px;

                        box-shadow:
                            0 5px 20px rgba(0,0,0,0.08);

                        text-align: center;
                    }

                    h1 {

                        color: #2563EB;
                    }

                    p {

                        color: #475569;

                        margin-top: 15px;
                    }

                </style>

            </head>

            <body>

                <div class="card">

                    <h1>
                        Zerodha Connected Successfully
                    </h1>

                    <p>
                        Session generated successfully.
                    </p>

                    <p>
                        You can close this window now.
                    </p>

                </div>

            </body>

            </html>
            """

        return f"""
        <h2>
            Session generation failed
        </h2>

        <p>
            {response.get("error")}
        </p>
        """

    except Exception as e:

        print(
            "\n========== CALLBACK ERROR =========="
        )

        print(str(e))

        return f"""
        <h2>
            Unexpected Error
        </h2>

        <p>
            {str(e)}
        </p>
        """


if __name__ == "__main__":

    print(
        "\n========== STARTING CALLBACK SERVER =========="
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )