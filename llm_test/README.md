# Using LLMs to Identify Misinformation

## Setting Up OpenAI
In this project, we tested various [LLM models from OpenAI](https://platform.openai.com/docs/models/overview). To run this code, you will have to [create an OpenAI account](https://platform.openai.com/signup) and purchase a small amount of tokens. **If you don't want to test OpenAI models, you can skip this section.**

Once you have created an account and generated your own OpenAI API key, open your terminal and run:

    export OPENAI_API_KEY=<your-api-key>

#### OpenAI Models We Tested
- [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)
- [gpt-4-turbo](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4)

## Setting Up Ollama
In this project, we tested varios [LLMs from Ollama](https://ollama.com/library). To run this code, you will have to [download the Ollama software](https://ollama.com/) and then download each LLM you would like to test. **If you don't want to test Ollama models, you can skip this section.**

- [Download Ollama](https://ollama.com/)

To download the specific LLM you want to test, run the following in your terminal:

    ollama run <model-name>

#### Ollama Models We Tested:
- [mistral:instruct](https://ollama.com/library/mistral)
- [llama3:8b](https://ollama.com/library/llama3)
- [llama2:7b](https://ollama.com/library/llama2)

## Running the Baseline Testing Script
Before running any scripts, make sure you have installed the requirements. Refer [here](https://github.com/isaacharlem/llm-as-judge-fake-news/blob/master/README.md) for instruction on how to do so.

In your terminal, navigate to the project directory:

    cd <project-directory>

Once in the project directory:

    python llm_test/baseline_llm_test.py

- When prompted, enter the exact name of the LLM you would like to test.

- When prompted, enter the number of iterations you would like the LLM to loop through when evaluating each headline. Note that if you are performing OpenAI API calls, a higher number of iterations will cost more money and the amount of time it will take to run the script will linearly increase. We used 100 iterations during testing as a default.

*If you have all the requirements installed, this file should run and produce a csv with the results in `data` folder of this project's directory.*

## Running the LLM Chain Testing Script
Before running the [LLM Chain Testing Script](https://github.com/isaacharlem/llm-as-judge-fake-news/blob/master/llm_test/chain_llm_test.py), make sure you have already ran the [LLM Baseline Testing Script](https://github.com/isaacharlem/llm-as-judge-fake-news/blob/master/llm_test/baseline_llm_test.py) for the desired model as described above. The information collected from the LLM Baseline Testing Script is essential to running the LLM Chain Testing Script, so it must be run before preceding with this step. 

Additionally, make sure that this script has not already been run for model you would like to test. If it has already been run, you must first delete the `model_chain_c` and `model_chain_std` columns from the appropriate csv in order to rerun the code. 

Some older LLM models are incompatible with this script because they are unable to consistently generate reliable data in the serializable format. **Please refrain from testing llama2 with this script.** All other models that have been previously tested will work.

In your terminal, navigate to the project directory:

    cd <project-directory>

Once in the project directory:

    python llm_test/chain_llm_test.py

- When prompted, enter the exact name of the LLM you would like to test.

- When prompted, enter the number of iterations you would like the LLM to loop through when evaluating each headline. Note that if you are performing OpenAI API calls, a higher number of iterations will cost more money and the amount of time it will take to run the script will linearly increase. We used 100 iterations during testing as a default.

*If you have all the requirements installed, this file should run and produce a csv with the results in `data` folder of this project's directory.*