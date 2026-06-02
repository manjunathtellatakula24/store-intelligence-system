import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import cv2

st.set_page_config(
    page_title="AI Store Intelligence",
    page_icon="🛍️",
    layout="wide"
)

st_autorefresh(
    interval=3000,
    key="dashboard_refresh"
)

st.title("🛍️ AI Store Intelligence Dashboard")

# CCTV

st.subheader("📹 Store CCTV Feed")

video = cv2.VideoCapture(
    "data/videos/store.mp4"
)

ret, frame = video.read()

if ret:

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    st.image(
        frame,
        channels="RGB",
        use_container_width=True
    )

video.release()

st.markdown("---")

try:

    events = requests.get(
        "http://127.0.0.1:8000/events"
    ).json()

    metrics = requests.get(
        "http://127.0.0.1:8000/metrics"
    ).json()

    funnel = requests.get(
        "http://127.0.0.1:8000/funnel"
    ).json()

    conversion = requests.get(
        "http://127.0.0.1:8000/conversion"
    ).json()

    health = requests.get(
        "http://127.0.0.1:8000/health"
    ).json()
    journey = requests.get(
        "http://127.0.0.1:8000/journey"
    ).json()

    df = pd.DataFrame(events)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "👥 Visitors",
        metrics["total_visitors"]
    )

    col2.metric(
        "📊 Events",
        metrics["total_events"]
    )

    col3.metric(
        "🏪 Zones",
        df["zone_id"].nunique()
        if not df.empty else 0
    )

    col4.metric(
        "🛒 Conversion %",
        conversion["conversion_rate"]
    )

    col5.metric(
        "💚 Health",
        health["status"]
    )
    col6.metric(
        "👨‍💼 Staff",
        metrics["staff_count"]
    )

    st.markdown("---")

    st.subheader("🎯 Conversion Funnel")

    funnel_df = pd.DataFrame(
        {
            "Stage": [
                "Entered",
                "Zone Visit",
                "Billing Queue",
                "Purchased"
            ],
            "Count": [
                funnel["entered"],
                funnel["zone_visits"],
                funnel["billing_queue"],
                funnel["purchased"]
            ]
        }
    )

    st.bar_chart(
        funnel_df.set_index("Stage")
    )

    st.markdown("---")

    st.subheader("📋 Event Stream")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    if not df.empty:

        st.subheader("🔥 Zone Analytics")

        zone_counts = (
            df["zone_id"]
            .value_counts()
        )

        st.bar_chart(
            zone_counts
        )

        st.subheader("🏆 Most Visited Zone")

        st.success(
            zone_counts.idxmax()
        )

    st.markdown("---")

    st.subheader("📈 Business KPIs")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Store Entries",
        funnel["entered"]
    )

    c2.metric(
        "Purchases",
        funnel["purchased"]
    )

    c3.metric(
        "Conversion Rate",
        f"{conversion['conversion_rate']}%"
    )

    st.markdown("---")

    st.subheader("🛒 Customer Journey Analytics")

    for visitor, path in journey.items():

        st.write(
            f"{visitor} : {' → '.join(path)}"
        )

except Exception as e:

    st.error(str(e))