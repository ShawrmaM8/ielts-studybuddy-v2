import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def calculate_band_score(correct: int, total: int) -> float:
    """Calculate IELTS band score based on raw score."""
    percentage = (correct / total) * 100
    if total == 40:  # Standard IELTS Reading/Listening test
        if percentage >= 97.5: return 9.0
        elif percentage >= 92.5: return 8.5
        elif percentage >= 87.5: return 8.0
        elif percentage >= 80: return 7.5
        elif percentage >= 72.5: return 7.0
        elif percentage >= 65: return 6.5
        elif percentage >= 57.5: return 6.0
        elif percentage >= 50: return 5.5
        return 5.0
    return round(percentage / 10, 1)

def generate_visualizations(section: str, results: Dict, times: List[float]) -> None:
    """Generate performance visualizations using Matplotlib/Seaborn."""
    output_dir = Path("visualizations")
    output_dir.mkdir(exist_ok=True)

    # Accuracy per question
    df = pd.DataFrame.from_dict(results, orient="index")
    plt.figure(figsize=(10, 6))
    sns.barplot(x=df.index, y=df["is_correct"].astype(int), hue=df["is_correct"])
    plt.title(f"{section} Accuracy per Question")
    plt.xlabel("Question Number")
    plt.ylabel("Correct (1) / Incorrect (0)")
    plt.savefig(output_dir / f"{section}_accuracy.png", bbox_inches="tight")
    plt.close()

    # Time per question
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=range(1, len(times) + 1), y=times)
    plt.title(f"{section} Time per Question (seconds)")
    plt.xlabel("Question Number")
    plt.ylabel("Time (seconds)")
    plt.savefig(output_dir / f"{section}_time.png", bbox_inches="tight")
    plt.close()