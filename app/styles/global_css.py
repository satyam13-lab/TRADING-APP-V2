def load_css():

    return """
    <style>

    .stApp {
        background-color: #F5F9FF;
        color: #111827;
    }

    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    .main-title {

        font-size: 46px;
        font-weight: 800;

        color: #0F172A;

        margin-bottom: 0px;
    }

    .sub-title {

        color: #64748B;

        font-size: 18px;

        margin-top: 5px;

        margin-bottom: 35px;
    }

    .metric-card {

        background: white;

        border-radius: 22px;

        padding: 28px;

        border-left: 5px solid #2563EB;

        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.05);

        min-height: 150px;

        margin-bottom: 20px;
    }

    .metric-label {

        color: #64748B;

        font-size: 15px;

        margin-bottom: 10px;
    }

    .metric-value {

        color: #0F172A;

        font-size: 30px;

        font-weight: 700;

        margin: 0;
    }

    .metric-sub {

        color: #64748B;

        font-size: 16px;

        margin-top: 8px;
    }

    .status-connected {

        color: #16A34A;

        font-weight: 700;

        font-size: 28px;
    }

    .status-disconnected {

        color: #DC2626;

        font-weight: 700;

        font-size: 28px;
    }

    .card {

        background: white;

        border-radius: 22px;

        padding: 30px;

        border: 1px solid #E2E8F0;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.05);

        margin-bottom: 20px;
    }

    .section-title {

        font-size: 34px;

        font-weight: 700;

        color: #0F172A;
    }

    .section-subtitle {

        color: #64748B;

        font-size: 18px;

        margin-bottom: 25px;
    }

    .info-box {

        background: #EFF6FF;

        border: 1px solid #BFDBFE;

        padding: 22px;

        border-radius: 16px;

        color: #1E40AF;

        margin-top: 20px;
        margin-bottom: 20px;
    }

    .success-box {

        background: #ECFDF5;

        border: 1px solid #BBF7D0;

        padding: 16px;

        border-radius: 14px;

        color: #15803D;

        margin-top: 20px;
    }

    .sidebar-title {

        font-size: 30px;

        font-weight: 800;

        color: #1E3A8A;
    }

    .sidebar-subtitle {

        color: #2563EB;

        font-size: 18px;

        margin-bottom: 30px;
    }

    .module-item {

        font-size: 18px;

        padding: 10px 0;

        color: #334155;
    }

    .workspace-header {
        border-bottom: 1px solid #D8E1EE;
        padding-bottom: 18px;
        margin-bottom: 24px;
    }

    .workspace-title {
        color: #0F172A;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .workspace-subtitle {
        color: #64748B;
        font-size: 16px;
    }

    .panel {
        background: #FFFFFF;
        border: 1px solid #DDE7F3;
        border-radius: 8px;
        padding: 20px;
        min-height: 120px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
        margin-bottom: 18px;
    }

    .panel-title {
        color: #0F172A;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .panel-subtitle {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 14px;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        border: 1px solid #CBD5E1;
        background: #F8FAFC;
        color: #334155;
    }

    .status-green {
        background: #ECFDF5;
        border-color: #BBF7D0;
        color: #15803D;
    }

    .status-amber {
        background: #FFFBEB;
        border-color: #FDE68A;
        color: #B45309;
    }

    .status-red {
        background: #FEF2F2;
        border-color: #FECACA;
        color: #B91C1C;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #DDE7F3;
        border-radius: 8px;
        overflow: hidden;
    }

    </style>
    """
