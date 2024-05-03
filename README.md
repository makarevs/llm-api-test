# Using OpenAI API with EPAM-hosted LLAMA LLM

This Python script demonstrates how to use the OpenAI API to make requests to the EPAM-hosted LLAMA LLM model for both completions and chat completions.

## Installation

1. Ensure you have Python 3.x installed.

2. Install the 'openai' package using pip:
    ```
    pip install openai
    ```

3. Add your API key to the `main.py` script. Replace `"EMPTY"` with your actual API key.

4. Run the script:
    ```
    python main.py
    ```

## Use Cases with Examples

### code completion

Prompt: "Write a python function that adds two numbers"
The script sends a completion request to the LLAMA model and receives a Python function that adds two numbers.

### chat completions

Prompt: "What is the best food in Paris?"
The script sends a chat completion request to the LLAMA model and receives a response suggesting the best food in Paris.

## LangChain Installation
https://python.langchain.com/docs/get_started/installation

### To install LangChain run

Some parts may need special option
```
********************************************************************************
Requirements should be satisfied by a PEP 517 installer.
If you are using pip, you can try `pip install --use-pep517`.
********************************************************************************
```

```
pip  --use-pep517 install langchain transformers numpy pandas datasets faiss-gpu
```

```
conda install langchain -c conda-forge
```

This will install the bare minimum requirements of LangChain. A lot of the value of LangChain comes when integrating it with various model providers, datastores, etc. By default, the dependencies needed to do that are NOT installed. However, there are two other ways to install LangChain that do bring in those dependencies.

To install modules needed for the common LLM providers, run:

```
pip install langchain[llms]
```

To install all modules needed for all integrations, run:

```
pip install langchain[all]
```

Note that if you are using zsh, you'll need to quote square brackets when passing them as an argument to a command, for example:

```
pip install 'langchain[all]'
```