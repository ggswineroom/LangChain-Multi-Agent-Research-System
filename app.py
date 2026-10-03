import streamlit as st
from src.pipelines.pipeline import run_research_pipeline


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #777;
            margin-bottom: 2rem;
        }

        .step-card {
            padding: 1rem;
            border-radius: 10px;
            background-color: #f7f7f7;
            border: 1px solid #e5e5e5;
            margin-bottom: 1rem;
        }

        .result-box {
            padding: 1.2rem;
            border-radius: 10px;
            background-color: #fafafa;
            border: 1px solid #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">🔎 AI Research Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Search the web, extract detailed information, generate a report, '
    'and have an AI critic review the result.'
    '</div>',
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Research Settings")

    topic = st.text_area(
        "Research Topic",
        placeholder="Example: The impact of AI on software development",
        height=120,
    )

    run_button = st.button(
        "🚀 Start Research",
        use_container_width=True,
        type="primary",
    )

    st.divider()

    st.markdown(
        """
        ### Pipeline

        **1. 🔎 Search Agent**  
        Finds recent and reliable information.

        **2. 📖 Reader Agent**  
        Selects a relevant source and extracts deeper content.

        **3. ✍️ Writer**  
        Creates the research report.

        **4. 🧐 Critic**  
        Reviews the generated report.
        """
    )


# -----------------------------
# Main Application
# -----------------------------
if run_button:

    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    st.session_state["research_state"] = None

    # Progress UI
    progress = st.progress(0)
    status = st.empty()

    status.info("🔎 Running research pipeline...")

    try:
        # -------------------------------------------------
        # Call your existing pipeline WITHOUT modifying it
        # -------------------------------------------------
        result = run_research_pipeline(topic.strip())

        progress.progress(100)
        status.success("✅ Research completed successfully!")

        st.session_state["research_state"] = result

    except Exception as e:
        progress.progress(0)

        st.error(
            f"❌ An error occurred while running the research pipeline:\n\n{e}"
        )

        st.stop()


# -----------------------------
# Display Results
# -----------------------------
if st.session_state.get("research_state"):

    result = st.session_state["research_state"]

    st.divider()

    st.header("📊 Research Results")

    # -------------------------------------------------
    # Search Results
    # -------------------------------------------------
    with st.expander("🔎 Search Results", expanded=False):

        search_results = result.get("search_results", "")

        if search_results:
            st.markdown(search_results)
        else:
            st.info("No search results available.")


    # -------------------------------------------------
    # Scraped Content
    # -------------------------------------------------
    with st.expander("📖 Detailed Scraped Content", expanded=False):

        scraped_content = result.get("scraped_content", "")

        if scraped_content:
            st.markdown(scraped_content)
        else:
            st.info("No scraped content available.")


    # -------------------------------------------------
    # Final Report
    # -------------------------------------------------
    st.header("📝 Final Research Report")

    report = result.get("report", "")

    if report:
        st.markdown(
            f'<div class="result-box">{report}</div>',
            unsafe_allow_html=True,
        )

        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
        )

    else:
        st.info("No report was generated.")


    # -------------------------------------------------
    # Critic Feedback
    # -------------------------------------------------
    st.header("🧐 Critic Review")

    feedback = result.get("feedback", "")

    if feedback:
        st.markdown(
            f'<div class="result-box">{feedback}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("No critic feedback available.")
