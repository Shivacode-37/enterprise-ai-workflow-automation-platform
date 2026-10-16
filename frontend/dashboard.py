import os

import json

import html

import requests

import streamlit as st


def render_readable_json(data):
    """Render JSON with reliable contrast in both dashboard themes."""
    json_text = json.dumps(data, indent=2, ensure_ascii=False)
    st.markdown(
        f"""
        <div style="
            color: #172B4D !important;
            background-color: #FFFFFF !important;
            border: 1px solid #C5D0DF;
            border-radius: 8px;
            padding: 16px;
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            font-family: Consolas, 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
        ">{html.escape(json_text)}</div>
        """,
        unsafe_allow_html=True,
    )


API_BASE_URL = os.getenv(

    "API_BASE_URL",

    "http://127.0.0.1:8000",

)

st.set_page_config(

    page_title="Enterprise AI Workflow",

    page_icon="🤖",

    layout="wide",

)

st.title("Enterprise AI Workflow Automation")

st.caption(

    "AI-powered IT asset requests, approvals, and workflow monitoring"

)

st.sidebar.header("Navigation")

if "dashboard_theme" not in st.session_state:

    st.session_state["dashboard_theme"] = "Dark"

dashboard_theme = st.sidebar.radio(

    "Appearance",

    options=["Dark", "Light"],

    horizontal=True,

    key="dashboard_theme",

)

# Centralized dashboard theme*

if dashboard_theme == "Dark":

    theme = {

        "bg": "#0B1220",

        "sidebar": "#101A2B",

        "surface": "#151F30",

        "surface_alt": "#1B2940",

        "text": "#F1F5F9",

        "muted": "#B6C3D6",

        "border": "#40516B",

        "input": "#111C2E",

        "placeholder": "#A8B6CC",

        "primary": "#60A5FA",

        "hover": "#243650",

    }

else:

    theme = {

        "bg": "#F3F6FC",

        "sidebar": "#FFFFFF",

        "surface": "#FFFFFF",

        "surface_alt": "#EDF2F9",

        "text": "#172B4D",

        "muted": "#526581",

        "border": "#C5D0DF",

        "input": "#FFFFFF",

        "placeholder": "#64748B",

        "primary": "#2563EB",

        "hover": "#E7EEF9",

    }

theme_css = f"""

<style>

/* ===== Application backgrounds ===== */

.stApp,

[data-testid="stAppViewContainer"],

[data-testid="stMain"],

[data-testid="stMainBlockContainer"] {{

    background-color: {theme["bg"]} !important;

    color: {theme["text"]} !important;

}}

[data-testid="stSidebar"],

[data-testid="stSidebar"] > div {{

    background-color: {theme["sidebar"]} !important;

    color: {theme["text"]} !important;

}}

[data-testid="stHeader"] {{

    background-color: {theme["bg"]} !important;

}}

/* ===== All standard text ===== */

.stApp,

.stApp p,

.stApp label,

.stApp span,

.stApp li,

.stApp .stMarkdown,

.stApp [data-testid="stCaptionContainer"],

.stApp [data-testid="stMetricLabel"],

.stApp [data-testid="stMetricValue"] {{

    color: {theme["text"]};

}}

.stApp [data-testid="stCaptionContainer"] {{

    color: {theme["muted"]} !important;

}}

/* ===== Text inputs, text areas, number inputs ===== */

.stApp input,

.stApp textarea,

.stApp [data-baseweb="input"] > div,

.stApp [data-baseweb="textarea"] > div {{

    background-color: {theme["input"]} !important;

    color: {theme["text"]} !important;

    -webkit-text-fill-color: {theme["text"]} !important;

    border-color: {theme["border"]} !important;

    border-radius: 8px !important;

}}

.stApp input::placeholder,

.stApp textarea::placeholder {{

    color: {theme["placeholder"]} !important;

    -webkit-text-fill-color: {theme["placeholder"]} !important;

    opacity: 1 !important;

}}

.stApp input:focus,

.stApp textarea:focus {{

    border-color: {theme["primary"]} !important;

    box-shadow: 0 0 0 1px {theme["primary"]} !important;

}}

/* ===== Select boxes and multi-selects ===== */

.stApp [data-baseweb="select"] > div {{

    background-color: {theme["input"]} !important;

    color: {theme["text"]} !important;

    border-color: {theme["border"]} !important;

}}

.stApp [data-baseweb="select"] input,

.stApp [data-baseweb="select"] span {{

    color: {theme["text"]} !important;

    -webkit-text-fill-color: {theme["text"]} !important;

}}

.stApp [data-baseweb="select"] svg {{

    fill: {theme["text"]} !important;

}}

/* Dropdown popup and options */

[data-baseweb="popover"],

[data-baseweb="menu"],

ul[role="listbox"] {{

    background-color: {theme["surface"]} !important;

    color: {theme["text"]} !important;

    border: 1px solid {theme["border"]} !important;

}}

li[role="option"],

[data-baseweb="menu"] li {{

    background-color: {theme["surface"]} !important;

    color: {theme["text"]} !important;

}}

li[role="option"]:hover,

[data-baseweb="menu"] li:hover {{

    background-color: {theme["hover"]} !important;

    color: {theme["text"]} !important;

}}

/* ===== Buttons ===== */

.stApp [data-testid="stButton"] button {{

    background-color: {theme["surface"]} !important;

    color: {theme["text"]} !important;

    border: 1px solid {theme["border"]} !important;

    border-radius: 8px !important;

}}

.stApp [data-testid="stButton"] button:hover {{

    border-color: {theme["primary"]} !important;

    color: {theme["primary"]} !important;

}}

.stApp [data-testid="stButton"] button[kind="primary"] {{

    background-color: {theme["primary"]} !important;

    color: #FFFFFF !important;

    border-color: {theme["primary"]} !important;

}}

/* ===== Cards, containers and visible separators ===== */

.stApp [data-testid="stVerticalBlockBorderWrapper"],

.stApp [data-testid="stExpander"],

.stApp [data-testid="stMetric"] {{

    background-color: {theme["surface"]} !important;

    border-color: {theme["border"]} !important;

    border-radius: 10px !important;

}}

.stApp hr {{

    border-color: {theme["border"]} !important;

}}

/* ===== Tables and dataframe containers ===== */

.stApp [data-testid="stDataFrame"],

.stApp [data-testid="stTable"] {{

    border: 1px solid {theme["border"]} !important;

    border-radius: 8px !important;

    overflow: hidden;

}}

/* ===== Radio buttons, checkboxes and sliders ===== */

.stApp [data-testid="stRadio"],

.stApp [data-testid="stCheckbox"],

.stApp [data-testid="stSelectbox"],

.stApp [data-testid="stMultiSelect"] {{

    color: {theme["text"]} !important;

}}

/* ===== Tabs and expanders ===== */

.stApp [data-testid="stTabs"] button,

.stApp [data-testid="stExpander"] summary {{

    color: {theme["text"]} !important;

}}

.stApp [data-testid="stExpander"] {{

    border: 1px solid {theme["border"]} !important;

}}

/* ===== Alerts and help text remain readable ===== */

.stApp [data-testid="stAlert"] {{

    border-radius: 8px !important;

}}

</style>

"""

st.markdown(theme_css, unsafe_allow_html=True)

pages = [

    "Overview",

    "Create AI Request",

    "Asset Requests",

    "Approvals",

    "Inventory",

    "Workflow Runs",

    "Audit Logs"

]

if "navigation_page" not in st.session_state:

    st.session_state["navigation_page"] = "Overview"

page = st.sidebar.radio(

    "Select a page",

    pages,

    key="navigation_page",

)

def get_api_data(endpoint: str):

    try:

        response = requests.get(

            f"{API_BASE_URL}{endpoint}",

            timeout=10,

        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as exc:

        st.error(f"Unable to connect to the backend: {exc}")

        return None

if page == "Overview":

    st.markdown("## Operations Overview")

    st.caption(

        "Monitor IT inventory, employee requests, approvals, "

        "and workflow activity from one place."

    )

    if st.button("Refresh dashboard", type="primary"):

        st.rerun()

    # Fetch live data from the existing FastAPI endpoints.*

    assets_data = get_api_data("/assets/")

    requests_data = get_api_data("/asset-requests/")

    approvals_data = get_api_data("/approvals/")

    # Calculate metrics only when the relevant API responds.*

    if assets_data is not None:

        total_assets = len(assets_data)

        available_assets = sum(

            asset.get("status", "").upper() == "AVAILABLE"

            and asset.get("assigned_to") is None

            for asset in assets_data

        )

        assigned_assets = sum(

            asset.get("status", "").upper() == "ASSIGNED"

            or asset.get("assigned_to") is not None

            for asset in assets_data

        )

        maintenance_assets = sum(

            asset.get("status", "").upper() == "MAINTENANCE"

            for asset in assets_data

        )

    else:

        total_assets = available_assets = assigned_assets = None

        maintenance_assets = None

    pending_approvals = (

        sum(

            approval.get("status", "").upper() == "PENDING"

            for approval in approvals_data

        )

        if approvals_data is not None

        else None

    )

    # KPI cards.*

    st.markdown("### Inventory and approvals")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Total assets",

            total_assets if total_assets is not None else "—",

            help="All asset records returned by the API.",

        )

    with col2:

        st.metric(

            "Available assets",

            available_assets if available_assets is not None else "—",

            help="Assets available for allocation.",

        )

    with col3:

        st.metric(

            "Assigned assets",

            assigned_assets if assigned_assets is not None else "—",

            help="Assets already allocated to a user.",

        )

    with col4:

        st.metric(

            "Pending approvals",

            pending_approvals if pending_approvals is not None else "—",

            help="Requests awaiting an approval decision.",

        )

    st.divider()

    # Inventory charts.*

    st.markdown("### Inventory insights")

    if assets_data is None:

        st.warning(

            "Inventory metrics are unavailable because the assets "

            "API did not return data."

        )

    elif not assets_data:

        st.info("No assets are currently registered.")

    else:

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            st.markdown("#### Assets by type")

            type_counts = {}

            for asset in assets_data:

                asset_type = asset.get("asset_type", "UNKNOWN")

                type_counts[asset_type] = (

                    type_counts.get(asset_type, 0) + 1

                )

            st.bar_chart(type_counts, horizontal=True)

        with chart_col2:

            st.markdown("#### Assets by status")

            status_counts = {}

            for asset in assets_data:

                asset_status = asset.get("status", "UNKNOWN").upper()

                status_counts[asset_status] = (

                    status_counts.get(asset_status, 0) + 1

                )

            st.bar_chart(status_counts, horizontal=True)

        st.caption(

            f"{available_assets} available · "

            f"{assigned_assets} assigned · "

            f"{maintenance_assets} in maintenance"

        )

    st.divider()

    # Recent activity.*

    st.markdown("### Recent requests")

    if requests_data is None:

        st.warning("Request history is currently unavailable.")

    elif not requests_data:

        st.info(

            "No requests yet. Use Create AI Request to submit "

            "your first request."

        )

    else:

        recent_requests = sorted(

            requests_data,

            key=lambda item: str(item.get("created_at", "")),

            reverse=True,

        )[:8]

        request_columns = [

            "id",

            "request_type",

            "status",

            "priority",

            "user_id",

            "created_at",

        ]

        recent_table = [

            {

                column: request.get(column, "—")

                for column in request_columns

            }

            for request in recent_requests

        ]

        st.dataframe(

            recent_table,

            use_container_width=True,

            hide_index=True,

        )

        st.caption(

            f"Showing the latest {len(recent_table)} requests."

        )

    st.info(

        "Use the sidebar to create AI requests, process approvals, "

        "explore inventory, and inspect workflow runs and audit logs."

    )

elif page == "Create AI Request":

    st.subheader("Create an AI-Powered Asset Request")

    st.caption(

        "Submit an IT asset request. The AI analyzes your needs "

        "against company policy and creates a request for approval."

    )

    # Explain the demo environment*

    with st.container(border=True):

        st.markdown("### How this demo works")

        st.markdown(

            """

            1. ****Describe your need**** — Explain which asset you need and why.

            2. ****AI analysis**** — The system identifies the asset type,

               priority, and request details using IT asset policy.

            3. ****Approval**** — A pending approval is created.

            4. ****Inventory allocation**** — After approval, the workflow

               attempts to assign an available asset.

            """

        )

    # Fetch actual users from the existing database.*

    # This query uses the existing users table directly through the API*

    # only if a user-list endpoint is available.*

    user_response = None

    try:

        user_response = requests.get(

            f"{API_BASE_URL}/users/",

            timeout=10,

        )

    except requests.RequestException:

        pass

    users = []

    if user_response is not None and user_response.ok:

        users = user_response.json()

    if not users:

        st.info(

            "Demo mode: the current backend has a limited set of users. "

            "This page will use the existing demo account until a "

            "user-list endpoint is available."

        )

        user_id = 2

        approver_id = 2

        st.markdown("****Demo employee and approver:**** User ID 2")

        st.caption(

            "These values match the current demo setup. "

            "Multiple employees and manager accounts are planned "

            "for a future improvement."

        )

    else:

        user_options = {

            f"{user['name']} — {user['role']} (ID {user['id']})":

                user["id"]

            for user in users

        }

        selected_user = st.selectbox(

            "Requesting employee",

            options=list(user_options.keys()),

            help="Select an existing employee account for this demo.",

        )

        user_id = user_options[selected_user]

        approver_options = {

            label: uid

            for label, uid in user_options.items()

        }

        selected_approver = st.selectbox(

            "Approver",

            options=list(approver_options.keys()),

            help="Select an existing account to route the request to.",

        )

        approver_id = approver_options[selected_approver]

    st.divider()

    st.markdown("### Describe your request")

    user_text = st.text_area(

        "What asset do you need, and why?",

        placeholder=(

            "Example: I need a laptop for a new engineer joining "

            "the team because their role requires development work."

        ),

        height=140,

        help=(

            "Include the asset you need and a short business reason. "

            "The AI will analyze your description."

        ),

    )

    st.caption(

        "Supported asset types include laptop, monitor, keyboard, "

        "mouse, and headset."

    )

    if st.button(

        "Analyze and Create Request",

        type="primary",

        use_container_width=True,

    ):

        if len(user_text.strip()) < 5:

            st.warning("Please describe your request in more detail.")

        else:

            try:

                with st.spinner(

                    "Analyzing the request and creating approval..."

                ):

                    response = requests.post(

                        f"{API_BASE_URL}/ai/requests",

                        params={

                            "user_id": int(user_id),

                            "approver_id": int(approver_id),

                        },

                        json={"user_text": user_text.strip()},

                        timeout=90,

                    )

                if response.status_code == 201:

                    result = response.json()

                    request_data = result["asset_request"]

                    st.success("Your asset request was created.")

                    st.markdown("### Request confirmation")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(

                            "Request ID",

                            request_data.get("id", "Created"),

                        )

                    with col2:

                        st.metric(

                            "Request status",

                            request_data.get("status", "Submitted"),

                        )

                    st.markdown("### AI analysis")

                    render_readable_json(result["analysis"])

                    with st.expander("View request details"):

                        render_readable_json(request_data)

                    st.info(

                        "Your request and its pending approval are now "

                        "available in the Asset Requests and Approvals "

                        "pages. Workflow execution occurs after approval."

                    )

                else:

                    st.error(

                        f"Request failed ({response.status_code}): "

                        f"{response.text}"

                    )

            except requests.RequestException as exc:

                st.error(

                    f"Unable to connect to the backend: {exc}"

                )

elif page == "Asset Requests":

    st.markdown("## Asset Requests")

    st.caption(

        "Track employee requests, priorities, and approval progress."

    )

    if st.button("Refresh requests", type="primary"):

        st.rerun()

    data = get_api_data("/asset-requests/")

    if data is None:

        st.error(

            "Unable to load requests. Check the backend connection."

        )

    elif not data:

        st.info(

            "No asset requests yet. Create an AI request to get started."

        )

    else:

        requests_data = [dict(item) for item in data]

        def request_status(item):

            return str(item.get("status") or "UNKNOWN").upper()

        # Request summary cards.*

        total_requests = len(requests_data)

        pending_requests = sum(

            request_status(item) in {"PENDING", "PENDING_APPROVAL"}

            for item in requests_data

        )

        approved_requests = sum(

            request_status(item) == "APPROVED"

            for item in requests_data

        )

        rejected_requests = sum(

            request_status(item) == "REJECTED"

            for item in requests_data

        )

        st.markdown("### Request summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total requests", total_requests)

        col2.metric("Pending", pending_requests)

        col3.metric("Approved", approved_requests)

        col4.metric("Rejected", rejected_requests)

        st.divider()

        st.markdown("### Find a request")

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        all_statuses = sorted({

            request_status(item) for item in requests_data

        })

        all_types = sorted({

            str(item.get("request_type") or "UNKNOWN").upper()

            for item in requests_data

        })

        with filter_col1:

            search_id = st.text_input(

                "Search request ID or employee ID",

                placeholder="Enter an ID...",

                key="request_search",

            )

        with filter_col2:

            selected_status = st.selectbox(

                "Status",

                ["All statuses"] + all_statuses,

                key="request_status_filter",

            )

        with filter_col3:

            selected_type = st.selectbox(

                "Asset type",

                ["All types"] + all_types,

                key="request_type_filter",

            )

        filtered_requests = requests_data

        if search_id.strip():

            search_value = search_id.strip().casefold()

            filtered_requests = [

                item for item in filtered_requests

                if search_value in str(item.get("id", "")).casefold()

                or search_value in str(

                    item.get("user_id", "")

                ).casefold()

            ]

        if selected_status != "All statuses":

            filtered_requests = [

                item for item in filtered_requests

                if request_status(item) == selected_status

            ]

        if selected_type != "All types":

            filtered_requests = [

                item for item in filtered_requests

                if str(

                    item.get("request_type") or "UNKNOWN"

                ).upper() == selected_type

            ]

        st.caption(

            f"Showing {len(filtered_requests)} of "

            f"{total_requests} requests"

        )

        # Display only fields returned by the existing API.*

        preferred_columns = [

            "id",

            "request_type",

            "status",

            "priority",

            "user_id",

            "created_at",

        ]

        available_columns = [

            column for column in preferred_columns

            if any(column in item for item in filtered_requests)

        ]

        table_data = [

            {column: item.get(column) for column in available_columns}

            for item in filtered_requests

        ]

        if table_data:

            st.dataframe(

                table_data,

                use_container_width=True,

                hide_index=True,

            )

        else:

            st.info("No requests match the selected filters.")

elif page == "Approvals":

    st.markdown("## Approval Management")

    st.caption(

        "Review asset requests, track approval decisions, "

        "and approve or reject pending requests."

    )

    col_refresh, col_info = st.columns([1, 4])

    with col_refresh:

        if st.button("Refresh approvals", use_container_width=True):

            st.rerun()

    data = get_api_data("/approvals/")

    if data is not None:

        if not data:

            st.info("No approvals found.")

        else:

            # Summary metrics*

            total_approvals = len(data)

            pending_count = sum(

                1 for item in data

                if item.get("status", "").upper() == "PENDING"

            )

            approved_count = sum(

                1 for item in data

                if item.get("status", "").upper() == "APPROVED"

            )

            rejected_count = sum(

                1 for item in data

                if item.get("status", "").upper() == "REJECTED"

            )

            metric_cols = st.columns(4)

            with metric_cols[0]:

                st.metric("Total Approvals", total_approvals)

            with metric_cols[1]:

                st.metric("Pending", pending_count)

            with metric_cols[2]:

                st.metric("Approved", approved_count)

            with metric_cols[3]:

                st.metric("Rejected", rejected_count)

            st.divider()

            # Search and filters*

            st.markdown("### Find Approvals")

            filter_col1, filter_col2 = st.columns([1, 2])

            with filter_col1:

                status_filter = st.selectbox(

                    "Approval Status",

                    options=[

                        "ALL",

                        "PENDING",

                        "APPROVED",

                        "REJECTED",

                    ],

                    key="approval_status_filter",

                )

            with filter_col2:

                search_text = st.text_input(

                    "Search approvals",

                    placeholder="Enter approval ID, request ID, or approver ID",

                    key="approval_search",

                ).strip().lower()

            filtered_data = []

            for approval in data:

                status = str(approval.get("status", "")).upper()

                if status_filter != "ALL" and status != status_filter:

                    continue

                searchable_text = " ".join(

                    str(approval.get(field, ""))

                    for field in ["id", "request_id", "approver_id"]

                ).lower()

                if search_text and search_text not in searchable_text:

                    continue

                filtered_data.append(approval)

            st.caption(

                f"Showing {len(filtered_data)} of {total_approvals} approvals"

            )

            if not filtered_data:

                st.info("No approvals match your search or selected filter.")

            # Approval cards*

            for approval in filtered_data:

                approval_id = approval.get("id")

                request_id = approval.get("request_id")

                approver_id = approval.get("approver_id")

                status = str(approval.get("status", "UNKNOWN")).upper()

                comments_saved = approval.get("comments")

                with st.container(border=True):

                    header_col, status_col = st.columns([3, 1])

                    with header_col:

                        st.markdown(f"****Approval #{approval_id}****")

                        st.caption(f"Related request: #{request_id}")

                    with status_col:

                        if status == "PENDING":

                            st.warning("PENDING")

                        elif status == "APPROVED":

                            st.success("APPROVED")

                        elif status == "REJECTED":

                            st.error("REJECTED")

                        else:

                            st.info(status)

                    detail_col1, detail_col2 = st.columns(2)

                    with detail_col1:

                        st.write(f"****Request ID:**** {request_id}")

                    with detail_col2:

                        st.write(f"****Approver ID:**** {approver_id}")

                    if comments_saved:

                        st.markdown("****Decision comments****")

                        st.write(comments_saved)

                    if status == "PENDING":

                        st.divider()

                        st.markdown("****Review this request****")

                        comments = st.text_area(

                            "Decision comments",

                            key=f"comments_{approval_id}",

                            placeholder=(

                                "Optional: explain your approval or "

                                "rejection decision."

                            ),

                        )

                        approve_col, reject_col = st.columns(2)

                        with approve_col:

                            if st.button(

                                "Approve Request",

                                key=f"approve_{approval_id}",

                                type="primary",

                                use_container_width=True,

                            ):

                                try:

                                    response = requests.patch(

                                        f"{API_BASE_URL}/approvals/"

                                        f"{approval_id}/decision",

                                        json={

                                            "status": "APPROVED",

                                            "comments": comments.strip() or None,

                                        },

                                        timeout=30,

                                    )

                                    if response.ok:

                                        st.success("Approval granted.")

                                        st.rerun()

                                    else:

                                        st.error(

                                            f"Failed ({response.status_code}): "

                                            f"{response.text}"

                                        )

                                except requests.RequestException as exc:

                                    st.error(

                                        f"Backend connection failed: {exc}"

                                    )

                        with reject_col:

                            if st.button(

                                "Reject Request",

                                key=f"reject_{approval_id}",

                                use_container_width=True,

                            ):

                                try:

                                    response = requests.patch(

                                        f"{API_BASE_URL}/approvals/"

                                        f"{approval_id}/decision",

                                        json={

                                            "status": "REJECTED",

                                            "comments": comments.strip() or None,

                                        },

                                        timeout=30,

                                    )

                                    if response.ok:

                                        st.success("Approval rejected.")

                                        st.rerun()

                                    else:

                                        st.error(

                                            f"Failed ({response.status_code}): "

                                            f"{response.text}"

                                        )

                                except requests.RequestException as exc:

                                    st.error(

                                        f"Backend connection failed: {exc}"

                                    )

                    else:

                        st.caption(

                            "This approval has already been decided."

                        )

elif page == "Inventory":

    st.markdown("## Asset Inventory")

    st.caption(

        "Explore, search, and monitor the organization's IT assets."

    )

    if st.button("Refresh inventory", type="primary"):

        st.rerun()

    data = get_api_data("/assets/")

    if data is None:

        st.error(

            "Unable to load inventory. Check that the FastAPI "

            "backend is running and reachable."

        )

    elif not data:

        st.info("No inventory assets found.")

    else:

        # Normalize values for consistent filtering and display.*

        assets = []

        for asset in data:

            item = dict(asset)

            item["asset_type"] = str(

                item.get("asset_type") or "UNKNOWN"

            ).upper()

            item["status"] = str(

                item.get("status") or "UNKNOWN"

            ).upper()

            item["name"] = str(item.get("name") or "")

            item["serial_number"] = str(

                item.get("serial_number") or ""

            )

            assets.append(item)

        total_assets = len(assets)

        available_assets = sum(

            item["status"] == "AVAILABLE"

            and item.get("assigned_to") is None

            for item in assets

        )

        assigned_assets = sum(

            item["status"] == "ASSIGNED"

            or item.get("assigned_to") is not None

            for item in assets

        )

        maintenance_assets = sum(

            item["status"] == "MAINTENANCE"

            for item in assets

        )

        # Summary cards.*

        st.markdown("### Inventory summary")

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric("Total assets", total_assets)

        metric2.metric("Available", available_assets)

        metric3.metric("Assigned", assigned_assets)

        metric4.metric("Maintenance", maintenance_assets)

        st.divider()

        # Search and filters.*

        st.markdown("### Find an asset")

        search_col, type_col, status_col = st.columns(

            [2, 1, 1]

        )

        with search_col:

            search_text = st.text_input(

                "Search",

                placeholder="Asset name or serial number...",

                key="inventory_search",

            )

        asset_types = sorted(

            {item["asset_type"] for item in assets}

        )

        statuses = sorted(

            {item["status"] for item in assets}

        )

        with type_col:

            selected_type = st.selectbox(

                "Asset type",

                options=["All types"] + asset_types,

                key="inventory_type_filter",

            )

        with status_col:

            selected_status = st.selectbox(

                "Status",

                options=["All statuses"] + statuses,

                key="inventory_status_filter",

            )

        filtered_assets = assets

        if search_text.strip():

            query = search_text.strip().casefold()

            filtered_assets = [

                item

                for item in filtered_assets

                if query in item["name"].casefold()

                or query in item["serial_number"].casefold()

            ]

        if selected_type != "All types":

            filtered_assets = [

                item

                for item in filtered_assets

                if item["asset_type"] == selected_type

            ]

        if selected_status != "All statuses":

            filtered_assets = [

                item

                for item in filtered_assets

                if item["status"] == selected_status

            ]

        st.caption(

            f"Showing {len(filtered_assets)} of {total_assets} assets"

        )

        # Present a concise, recruiter-friendly table.*

        display_columns = [

            "id",

            "name",

            "asset_type",

            "serial_number",

            "status",

            "location",

            "assigned_to",

        ]

        display_data = [

            {

                column: item.get(column)

                for column in display_columns

            }

            for item in filtered_assets

        ]

        st.dataframe(

            display_data,

            use_container_width=True,

            hide_index=True,

            column_config={

                "id": st.column_config.NumberColumn("Asset ID"),

                "name": st.column_config.TextColumn("Asset name"),

                "asset_type": st.column_config.TextColumn("Category"),

                "serial_number": st.column_config.TextColumn(

                    "Serial number"

                ),

                "status": st.column_config.TextColumn("Status"),

                "location": st.column_config.TextColumn("Location"),

                "assigned_to": st.column_config.NumberColumn(

                    "Assigned user ID",

                    format="%d",

                ),

            },

        )

        if not filtered_assets:

            st.info(

                "No assets match these filters. Try a different "

                "search term, category, or status."

            )

elif page == "Workflow Runs":

    st.markdown("## Workflow Runs")

    st.caption(

        "Monitor workflow executions, review their outcomes, "

        "and identify failed asset-allocation processes."

    )

    col_refresh, col_info = st.columns([1, 4])

    with col_refresh:

        if st.button("Refresh workflow runs", use_container_width=True):

            st.rerun()

    data = get_api_data("/workflow-runs/")

    if data is not None:

        if not data:

            st.info("No workflow runs found.")

        else:

            # Summary metrics*

            total_runs = len(data)

            completed_count = sum(

                1 for run in data

                if str(run.get("status", "")).upper() == "COMPLETED"

            )

            failed_count = sum(

                1 for run in data

                if str(run.get("status", "")).upper() == "FAILED"

            )

            running_count = sum(

                1 for run in data

                if str(run.get("status", "")).upper()

                in ["RUNNING", "PENDING", "IN_PROGRESS"]

            )

            metric_cols = st.columns(4)

            with metric_cols[0]:

                st.metric("Total Runs", total_runs)

            with metric_cols[1]:

                st.metric("Completed", completed_count)

            with metric_cols[2]:

                st.metric("Failed", failed_count)

            with metric_cols[3]:

                st.metric("In Progress", running_count)

            st.divider()

            # Search and filters*

            st.markdown("### Execution History")

            filter_col1, filter_col2 = st.columns([1, 2])

            available_statuses = sorted(

                {

                    str(run.get("status", "UNKNOWN")).upper()

                    for run in data

                }

            )

            with filter_col1:

                status_filter = st.selectbox(

                    "Execution Status",

                    options=["ALL"] + available_statuses,

                    key="workflow_status_filter",

                )

            with filter_col2:

                search_text = st.text_input(

                    "Search workflow runs",

                    placeholder="Enter run ID, request ID, or current step",

                    key="workflow_search",

                ).strip().lower()

            filtered_runs = []

            for run in data:

                status = str(run.get("status", "UNKNOWN")).upper()

                if status_filter != "ALL" and status != status_filter:

                    continue

                searchable_text = " ".join(

                    str(run.get(field, ""))

                    for field in [

                        "id",

                        "request_id",

                        "current_step",

                        "status",

                    ]

                ).lower()

                if search_text and search_text not in searchable_text:

                    continue

                filtered_runs.append(run)

            st.caption(

                f"Showing {len(filtered_runs)} of {total_runs} workflow runs"

            )

            if not filtered_runs:

                st.info(

                    "No workflow runs match your search or selected filter."

                )

            else:

                # Build a readable table from fields actually returned*

                preferred_columns = [

                    "id",

                    "request_id",

                    "status",

                    "current_step",

                    "started_at",

                    "completed_at",

                    "created_at",

                ]

                columns = [

                    column

                    for column in preferred_columns

                    if any(column in run for run in filtered_runs)

                ]

                # Preserve any additional API fields*

                extra_columns = [

                    column

                    for run in filtered_runs

                    for column in run.keys()

                    if column not in columns

                ]

                columns.extend(

                    column

                    for column in dict.fromkeys(extra_columns)

                    if column not in columns

                )

                st.dataframe(

                    [

                        {column: run.get(column) for column in columns}

                        for run in filtered_runs

                    ],

                    use_container_width=True,

                    hide_index=True,

                )

                # Detailed execution view*

                st.markdown("### Run Details")

                run_options = {

                    f"Run #{run.get('id', 'N/A')} — "

                    f"{str(run.get('status', 'UNKNOWN')).upper()} "

                    f"(Request #{run.get('request_id', 'N/A')})": run

                    for run in filtered_runs

                }

                selected_label = st.selectbox(

                    "Select a workflow run",

                    options=list(run_options.keys()),

                    key="selected_workflow_run",

                )

                selected_run = run_options[selected_label]

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:

                    st.write(f"****Run ID:**** {selected_run.get('id', 'N/A')}")

                    st.write(

                        f"****Request ID:**** "

                        f"{selected_run.get('request_id', 'N/A')}"

                    )

                    st.write(

                        f"****Status:**** "

                        f"{selected_run.get('status', 'UNKNOWN')}"

                    )

                with detail_col2:

                    st.write(

                        f"****Current Step:**** "

                        f"{selected_run.get('current_step') or 'Not specified'}"

                    )

                    st.write(

                        f"****Started At:**** "

                        f"{selected_run.get('started_at') or 'Not recorded'}"

                    )

                    st.write(

                        f"****Completed At:**** "

                        f"{selected_run.get('completed_at') or 'Not recorded'}"

                    )

                with st.expander("View complete run data"):

                    render_readable_json(selected_run)

elif page == "Audit Logs":

    st.markdown("## Audit Logs")

    st.caption(

        "Track workflow actions, asset allocation outcomes, "

        "and request-level activity for traceability."

    )

    # Filters*

    filter_col1, filter_col2 = st.columns([1, 1])

    with filter_col1:

        request_id_filter = st.number_input(

            "Filter by Request ID (0 = all requests)",

            min_value=0,

            value=0,

            step=1,

            key="audit_request_id_filter",

        )

    with filter_col2:

        limit = st.selectbox(

            "Maximum events to retrieve",

            options=[25, 50, 100, 200, 500],

            index=2,

            key="audit_limit",

        )

    if st.button("Refresh audit logs", use_container_width=False):

        st.rerun()

    # Fetch logs using the existing endpoint*

    endpoint = f"/audit-logs/?limit={limit}"

    if request_id_filter > 0:

        endpoint += f"&request_id={int(request_id_filter)}"

    data = get_api_data(endpoint)

    if data is not None:

        if not data:

            st.info("No audit events found for these filters.")

        else:

            # Summary metrics based on the fetched events*

            total_events = len(data)

            action_counts = {}

            for item in data:

                action = str(item.get("action", "UNKNOWN")).upper()

                action_counts[action] = action_counts.get(action, 0) + 1

            failed_events = sum(

                1

                for item in data

                if any(

                    word in str(item.get("action", "")).upper()

                    for word in ["FAILED", "ERROR"]

                )

            )

            unique_requests = {

                item.get("request_id")

                for item in data

                if item.get("request_id") is not None

            }

            metric_cols = st.columns(3)

            with metric_cols[0]:

                st.metric("Events Retrieved", total_events)

            with metric_cols[1]:

                st.metric("Distinct Requests", len(unique_requests))

            with metric_cols[2]:

                st.metric("Failure-Related Events", failed_events)

            st.divider()

            st.markdown("### Event Explorer")

            # Action filter and text search*

            available_actions = sorted(

                {

                    str(item.get("action", "UNKNOWN"))

                    for item in data

                }

            )

            control_col1, control_col2 = st.columns([1, 2])

            with control_col1:

                selected_actions = st.multiselect(

                    "Filter by action",

                    options=available_actions,

                    default=available_actions,

                    key="audit_action_filter",

                )

            with control_col2:

                search_text = st.text_input(

                    "Search audit events",

                    placeholder=(

                        "Search by event ID, request ID, action, "

                        "or details"

                    ),

                    key="audit_search",

                ).strip().lower()

            filtered_data = []

            for item in data:

                action = str(item.get("action", "UNKNOWN"))

                if action not in selected_actions:

                    continue

                searchable_text = " ".join(

                    str(value)

                    for key, value in item.items()

                    if key.lower() in {

                        "id",

                        "request_id",

                        "action",

                        "details",

                        "description",

                        "entity_type",

                        "entity_id",

                        "created_at",

                        "timestamp",

                    }

                ).lower()

                if search_text and search_text not in searchable_text:

                    continue

                filtered_data.append(item)

            st.caption(

                f"Showing {len(filtered_data)} of {total_events} "

                "retrieved events"

            )

            if not filtered_data:

                st.info(

                    "No audit events match the selected filters."

                )

            else:

                # Prefer common audit fields; retain other API fields*

                preferred_columns = [

                    "id",

                    "request_id",

                    "action",

                    "entity_type",

                    "entity_id",

                    "details",

                    "description",

                    "created_at",

                    "timestamp",

                ]

                columns = [

                    column

                    for column in preferred_columns

                    if any(column in item for item in filtered_data)

                ]

                extra_columns = [

                    key

                    for item in filtered_data

                    for key in item.keys()

                    if key not in columns

                ]

                columns.extend(

                    key

                    for key in dict.fromkeys(extra_columns)

                    if key not in columns

                )

                st.dataframe(

                    [

                        {column: item.get(column) for column in columns}

                        for item in filtered_data

                    ],

                    use_container_width=True,

                    hide_index=True,

                )

                # Expandable detail for individual events*

                st.markdown("### Event Details")

                event_options = {

                    (

                        f"Event #{item.get('id', 'N/A')} — "

                        f"{item.get('action', 'UNKNOWN')} "

                        f"(Request #{item.get('request_id', 'N/A')})"

                    ): item

                    for item in filtered_data

                }

                selected_event_label = st.selectbox(

                    "Select an event",

                    options=list(event_options.keys()),

                    key="selected_audit_event",

                )

                selected_event = event_options[selected_event_label]

                with st.container(border=True):

                    render_readable_json(selected_event)
