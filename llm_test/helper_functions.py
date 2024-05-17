"""Helper functions for running testing scripts."""

import pandas as pd
from prompt_templates import baseline_template, certainty_template
from collections import Counter
import os
import numpy as np

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOllama


def load_headlines(filepath="data/headlines.csv"):
    """
    Loads data into Pandas DataFrame from csv file.

    Inputs:
      filepath [string]: the filepath for the data

    Returns [DataFrame]: the relevant data in a Pandas DataFrame
    """
    headlines = pd.read_csv(filepath)

    return headlines


def invoke_llm(llm, headline, template, classification=None):
    """
    Invokes an LLM generation instance.

    Inputs:
      llm [LangChain Object]: the chat model for the LLM being tested
      headline [string]: the headline
      template [string]: the prompt template for the LLM

    Returns [string]: the relevant information extracted from the 
      response from an LLM.
    """
    messages = [
        SystemMessage(content=template),
        HumanMessage(content=headline),
    ]

    result = llm.invoke(messages)
    result = result.content.strip().replace(".", "")
    if classification:
        if result[0] not in ["1", "2", "3", "4", "5"]:
            print("\nRerunning LLM Chain Call Due to Format Issues")
            print(f"Incorrect Chain Response: {result}")
            invoke_llm(
                llm,
                headline,
                template
                + "YOU CAN ONLY RESPOND WITH ONE INTEGER BETWEEN 1 AND 5. DO NOT INCLUDE ANYTHING TEXT OR ADDITIONAL RESPONSE.",
                classification,
            )
        else:
            return int(result[0])
    else:
        if not (result.lower().startswith("real")) and not (
            result.lower().startswith("fake")
        ):
            print("\nRerunning LLM Call Due to Format Issues")
            print(f"Incorrect Response: {result}")
            invoke_llm(llm, headline, template)

        return result[:4]


def most_common_value_and_frequency(values):
    """
    Finds the most common value and its frequency in a list.

    Inputs:
      values [list[int]]: a list of values

    Returns:
      most_common [int]: the most common value
      frequency [float]: the frequency at which the most common value occured.
    """
    counter = Counter(values)
    most_common, count = counter.most_common(1)[0]
    frequency = count / len(values)

    return most_common, frequency


def evaluate_headlines(model, headlines, iterations, baseline, old_fp=None):
    """
    Evaluates a list of headlines using an LLM n times.

    Inputs:
      model [string]: the name of the LLM to be tested
      headlines [list[string]]: a list of headlines
      iterations [int]: the number of times the LLM should evaluate each headline.

    Returns:
      predicted [DataFrame]: the headlines with their corresponding LLM predictions
        and certainties
      model [string]: the name of the LLM that was tested
    """
    headlines_random = headlines.sample(n=20, replace=False)
    if not baseline:
        headlines_pred = load_headlines(old_fp + model + ".csv")
        if model == "llama2":
            raise ValueError(
                "The Llama2 Model is incompatible with this testing script. Please choose another model."
            )

    p_column = model + "_p"

    if "gpt" in model:
        llm = ChatOpenAI(model=model)
    else:
        llm = ChatOllama(model=model)

    results = []
    for headline in headlines_random.iloc[:, :1]["Headline"]:
        print(f"\nEvaluating Headline: {headline}")

        responses = []
        for _ in range(int(iterations)):
            if baseline:
                response = invoke_llm(llm, headline, baseline_template)
                responses.append(1 if response.lower() == "real" else 0)
            else:
                idx = headlines_pred[headlines_pred["Headline"] == headline].Real.index[
                    0
                ]
                classification = headlines_pred[headlines_pred["Headline"] == headline][
                    p_column
                ][idx]
                response = chain_llm(llm, headline, classification)
                responses.append(response)

        if baseline:
            prediction, certainty = most_common_value_and_frequency(responses)
            print(f"Prediction: {prediction}")
            print(f"Certainty: {certainty}\n")
            results.append((prediction, certainty))
        else:
            responses = list(map(lambda x: (x - 1) / 4, responses))
            responses_std = np.std(responses)
            results.append((np.mean(responses), responses_std))
            print(f"Baseline Classification: {classification}")
            print(f"Model-determined Certainty: {np.mean(responses)}")
            print(f"Model STD: {responses_std}")

    if baseline:
        headlines_random[model + "_p"] = [x[0] for x in results]
        headlines_random[model + "_c"] = [x[1] for x in results]
        predicted = pd.merge(
            headlines,
            headlines_random[[model + "_p", model + "_c"]],
            left_index=True,
            right_index=True,
        )
    else:
        headlines_random[model + "_chain_c"] = [x[0] for x in results]
        headlines_random[model + "_chain_std"] = [x[1] for x in results]
        predicted = pd.merge(
            headlines,
            headlines_random[[model + "_chain_c", model + "_chain_std"]],
            left_index=True,
            right_index=True,
        )

    return predicted, model


def save_data(data, model, filepath):
    """
    Saves the model predictions to a csv file.

    Inputs:
      data [DataFrame]: the original headlines data with the corresponding
        model predictions
      model [string]: the name of the model that was tested
      filepath [string]: the filepath for the output data

    Returns [None]
    """
    filepath = filepath + model + ".csv"

    if os.path.isfile(filepath):
        existing_data = pd.read_csv(filepath)
        new_data = pd.merge(
            existing_data, data.iloc[:, -2:], left_index=True, right_index=True
        ).drop(columns="Unnamed: 0")
        print("\n\n", new_data)
        new_data.to_csv(filepath, mode="w")
    else:
        data.to_csv(filepath)
        print("\n\n", data)

    print(f"\nData Saved: {filepath}")


def chain_llm(llm, headline, classification):
    """
    Chains the previous classification from the Baseline LLM with
    another evaluation to assess the LLM's confidence in its answer

    Inputs:
      llm [LangChain Object]: the chat model for the LLM being tested
      headline [string]: the headline

    Returns [string]: a integer rating represented as a string value
      from 1 to 5 based on how confident the LLM is of its previous answer.
    """
    pred = "real" if classification == 1 else "fake"
    check_response = certainty_template(pred)
    check_pred_1 = invoke_llm(llm, headline, check_response, True)

    return check_pred_1
