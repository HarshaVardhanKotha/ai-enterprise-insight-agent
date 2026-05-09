import streamlit as st
from rag_pipeline import answer_with_rag
from data_tools import load_metrics, summarize_metrics, region_report
from planner import create_action_plan

st.set_page_config(
    page_title="AI Enterprise Insight Agent",
    page_icon="✨",
    layout="wide"
)

st.markdown(
    '''
    <style>
    .main {
        background-color: #fafafa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    h1, h2, h3 {
        letter-spacing: -0.03em;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("AI Enterprise Insight Agent")
st.caption("A minimal GenAI system for enterprise knowledge search, business metrics, and action planning.")

tab1, tab2, tab3 = st.tabs(["Ask Knowledge Base", "Business Metrics", "AI Action Planner"])

with tab1:
    st.subheader("Ask enterprise documents")
    question = st.text_input(
        "Ask a question",
        placeholder="Example: What are the AI governance rules?"
    )

    if st.button("Generate grounded answer", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving context and generating answer..."):
                answer, sources = answer_with_rag(question)

            st.markdown("### Answer")
            st.write(answer)

            st.markdown("### Retrieved Sources")
            for source in sources:
                st.json(source)

with tab2:
    st.subheader("Structured business data")
    df = load_metrics()
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Summarize metrics", use_container_width=True):
            st.json(summarize_metrics())

    with col2:
        region = st.selectbox("Select region", df["region"].tolist())
        if st.button("Generate region report", use_container_width=True):
            st.json(region_report(region))

with tab3:
    st.subheader("Generate an action plan")
    problem = st.text_area(
        "Business problem",
        placeholder="Example: Customer satisfaction dropped in the South region."
    )

    if st.button("Create AI action plan", use_container_width=True):
        if not problem.strip():
            st.warning("Please enter a business problem.")
        else:
            with st.spinner("Creating action plan..."):
                plan = create_action_plan(problem)
            st.write(plan)
