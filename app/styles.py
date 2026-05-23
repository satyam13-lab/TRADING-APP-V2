def load_css():

    return """
    <style>

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin-bottom: 0;
    }

    .sub-title {
        color: #9CA3AF;
        font-size: 16px;
        margin-top: 0;
    }

    .card {
        background: linear-gradient(
            145deg,
            #111827,
            #1F2937
        );

        padding: 25px;
        border-radius: 16px;
        border: 1px solid #374151;

        box-shadow:
            0px 4px 20px rgba(0,0,0,0.25);

        margin-bottom: 20px;
    }

    .status-connected {
        color: #10B981;
        font-weight: 700;
        font-size: 18px;
    }

    .status-disconnected {
        color: #EF4444;
        font-weight: 700;
        font-size: 18px;
    }

    .metric-title {
        color: #9CA3AF;
        font-size: 14px;
    }

    .metric-value {
        color: white;
        font-size: 28px;
        font-weight: bold;
    }

    .stButton button {
        width: 100%;
        background: linear-gradient(
            90deg,
            #2563EB,
            #1D4ED8
        );

        color: white;
        border: none;
        border-radius: 10px;

        height: 50px;

        font-size: 16px;
        font-weight: 600;
    }

    .stButton button:hover {
        background: linear-gradient(
            90deg,
            #1D4ED8,
            #1E40AF
        );
    }

    </style>
    """