import streamlit as st
from passage_utils import extract_pdf
from passage_summarizer import summarize_passage
from lang_feedback import get_language_feedback
from flashcard import generate_flashcards  # Assuming this exists
from analyzer import IELTSAnalyzer
from analyzer_viz import plot_accuracy, plot_time_per_q, trap_insights
from datetime import datetime

st.title("IELTS Study Buddy")

# Initialize tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Text Extraction", "Summarization", "Flashcards", "Language Feedback", "Analyzer"])

with tab1:
    st.header("Text Extraction")
    uploaded_file = st.file_uploader("Upload PDF", type='pdf', key="extract_uploader")
    if uploaded_file:
        try:
            text = extract_pdf(uploaded_file.read())
            st.text_area("Extracted Text", text, height=200)
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("Summarization")
    text_input = st.text_area("Enter text to summarize", height=200, key="summarize_input")
    if st.button("Summarize"):
        summary = summarize_passage(text_input)
        st.write(summary)

with tab3:
    st.header("Flashcards")
    text_input = st.text_area("Enter text for flashcards", height=200, key="flashcard_input")
    if st.button("Generate Flashcards"):
        flashcards = generate_flashcards(text_input)  # Replace with your logic
        st.write(flashcards)

with tab4:
    st.header("Language Feedback")
    text_input = st.text_area("Enter text for feedback", height=200, key="feedback_input")
    if st.button("Get Feedback"):
        feedback = get_language_feedback(text_input)
        st.write(feedback)

with tab5:
    st.header("Automated Reading/Listening Analyzer")
    uploaded_file = st.file_uploader("Upload IELTS Practice PDF", type='pdf', key="analyzer_uploader")
    
    if uploaded_file:
        analyzer = IELTSAnalyzer()
        try:
            questions, answer_key = analyzer.extract_from_pdf(uploaded_file.read())
            st.success(f"Extracted {len(questions)} questions. Answer key sample: {list(answer_key.items())[:5]}")
        except Exception as e:
            st.error(f"Extraction error: {e}. Ensure PDF is text-based IELTS practice.")

        # User responses
        user_responses = {}
        start_time = datetime.now()
        for i, q in enumerate(questions[:10]):  # Limit for demo; scale as needed
            ans = st.text_input(f"Q{i+1}: {q[:100]}...", max_chars=5, key=f"analyzer_q{i}")
            user_responses[str(i+1)] = ans

        if st.button("Submit & Score", key="analyzer_submit"):
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            marks = analyzer.accept_responses(user_responses)
            band = analyzer.compute_band_score(marks, 'reading')
            st.metric("Band Score", band)
            st.write(f"Correct: {sum(marks.values())}/{len(marks)} | Total Time: {total_time:.1f}s")

            # Visualizations
            plot_accuracy(marks, questions)
            times = [total_time / len(marks)] * len(marks)  # Placeholder; add JS for per-Q timing
            plot_time_per_q(times)
            trap_insights(marks)