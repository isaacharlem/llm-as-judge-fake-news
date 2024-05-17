"""prompt_templates.py"""

baseline_template = """
Your job is to determine whether a news headlines is 'real' or 'fake'.

You will be provided a news headline. You must respond with either 'real' or 'fake'.
- real headlines are accurate and unbiased
- your response must be one word ONLY: either 'real' or 'fake'.
- Do not respond with any additional information or analysis.

Acceptable Responses:
- 'fake'
- 'real'
"""


def certainty_template(pred):
    certainty = f"""
    Your job is to rate how confident you are that a given news headline is '{pred}' on a scale of 1 to 5.

    You will be provided a news headline. You must respond with either '1', '2', '3', '4', or '5'.
    - 5 represents being most confident, 1 represents being least confident.
    - 'real' headlines are accurate and unbiased, 'fake' headlines are not accurate and/or biased.
    - your response must be only a single integer from 1 to 5.
    - Do not respond with any additional information or analysis.

    Acceptable Responses:
    - '1'
    - '2'
    - '3'
    - '4'
    - '5'
    """
    return certainty
