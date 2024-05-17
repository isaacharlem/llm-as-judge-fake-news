"""chain_llm_test.py"""

from helper_functions import *


if __name__ == "__main__":
    old_data_fp = "data/headlines_pred_"
    headlines = load_headlines()
    data, model = evaluate_headlines(
        input("LLM Model: "),
        headlines,
        input("Number of Iterations: "),
        False,
        old_data_fp,
    )
    save_data(data, model, old_data_fp)
