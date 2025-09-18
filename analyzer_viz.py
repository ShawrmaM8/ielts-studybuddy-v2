import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_accuracy(marks: dict, questions: list):
    """Plot accuracy per passage/section."""
    df = pd.DataFrame({'Question': list(marks.keys()), 'Correct': list(marks.values())})
    df['Section'] = ['Passage 1' if int(q) <= 13 else 'Passage 2' if int(q) <= 26 else 'Passage 3' for q in df['Question']]

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x='Section', y='Correct', ax=ax, estimator=lambda x: sum(x)/len(x)*100)
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy by Passage')
    plt.tight_layout()
    st.pyplot(fig)

def plot_time_per_q(times: list):
    """Plot time per question."""
    df = pd.DataFrame({'Question': range(1, len(times)+1), 'Time': times})
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=df, x='Question', y='Time', ax=ax)
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Time per Question')
    plt.tight_layout()
    st.pyplot(fig)

def trap_insights(marks: dict):
    """Highlight potential traps."""
    low_qs = [q for q, correct in marks.items() if not correct]
    if low_qs:
        st.write(f"Potential traps in questions: {', '.join(low_qs)}. Review for synonyms, distractors, or inference errors.")
    else:
        st.write("Great job! No major traps detected.")