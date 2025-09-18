import streamlit as st
from ielts_analyzer import IELTS_Analyzer
from pathlib import Path
import json

# Streamlit configuration
st.set_page_config(page_title="IELTS Analyzer", layout="wide")

# Initialize session state
if "analyzer" not in st.session_state:
    st.session_state.analyzer = None
if "section" not in st.session_state:
    st.session_state.section = "Reading"


def main():
    st.title("IELTS Reading & Listening Analyzer")

    # Tabs for Reading and Listening
    tab1, tab2 = st.tabs(["Reading", "Listening"])

    with tab1:
        process_section("Reading")

    with tab2:
        process_section("Listening")


def process_section(section: str):
    st.header(f"{section} Section")

    # File uploaders
    pdf_file = st.file_uploader(f"Upload {section} Practice PDF", type="pdf", key=f"{section}_pdf")
    answer_key_file = st.file_uploader(f"Upload Answer Key (JSON)", type="json", key=f"{section}_answer_key")

    if pdf_file and answer_key_file:
        # Save uploaded files
        pdf_path = Path(f"ielts_{section.lower()}_practice.pdf")
        answer_key_path = Path(f"{section.lower()}_answer_key.json")

        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        with open(answer_key_path, "wb") as f:
            f.write(answer_key_file.read())

        # Initialize analyzer
        st.session_state.analyzer = IELTS_Analyzer(str(pdf_path), str(answer_key_path))
        st.session_state.section = section

        # Extract questions
        try:
            text = st.session_state.analyzer.extract_text_from_pdf()
            questions = st.session_state.analyzer.extract_questions(text)
            st.session_state.analyzer.load_answer_key()

            st.subheader("Answer Questions")
            with st.form(key=f"{section}_form"):
                answers = {}
                for q in questions:
                    answers[q["number"]] = st.text_input(f"Question {q['number']}: {q['text']}",
                                                         key=f"{section}_q{q['number']}")
                submit_button = st.form_submit_button("Submit Answers")

                if submit_button:
                    st.session_state.analyzer.user_answers = answers
                    results = st.session_state.analyzer.mark_answers(section)
                    st.session_state.analyzer.generate_visualizations(section, results)

                    # Display results
                    st.subheader("Results")
                    st.write(
                        f"Raw Score: {st.session_state.analyzer.scores[section]['raw']}/{st.session_state.analyzer.scores[section]['total']}")
                    st.write(f"Band Score: {st.session_state.analyzer.scores[section]['band']}")

                    # Display visualizations
                    st.subheader("Visualizations")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(f"visualizations/{section}_accuracy.png", caption="Accuracy per Question")
                    with col2:
                        st.image(f"visualizations/{section}_time.png", caption="Time per Question")

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()