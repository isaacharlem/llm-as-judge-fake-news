"""Tests baseline LLM misinformation identification ability"""

from helper_functions import *


if __name__ == "__main__":
    headlines = load_headlines()
    data, model = evaluate_headlines(
        input("LLM Model: "), headlines, input("Number of Iterations: "), True
    )
    save_data(data, model, "data/headlines_pred_")
