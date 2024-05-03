import json
import faiss
from datasets import load_dataset
from langchain.batch.tree import LangChainIndex
from langchain.embedder import TransformerEmbedder
import openai

# Set the API key and API base URL for OpenAI
openai.api_key = "EMPTY"
openai.api_base = "https://api.llm.lab.epam.com/v1"

# Set the model name you want to use for the requests
model = "Llama-2-70B-chat-AWQ"

# Load, process, and save the COVID-QA dataset as a JSON file
def process_covid_qa_dataset():
    dataset = load_dataset("covid_qa_deepset")
    data = []

    for item in dataset['train']:
        document = {
            "title": item['title'],
            "text": item['context']
        }
        question = item['question']
        answer = item['answers']['text'][0]

        qa_pair = {
            "question": question,
            "answer": answer,
            "source": "covid_qa_deepset",
            "document": document
        }
        data.append(qa_pair)

    with open('covid_qa_dataset.json', 'w') as f:
        json.dump(data, f)

# Generate the Faiss index for the dataset using LangChain and the TransformerEmbedder
def generate_faiss_index(input_file, model_name, output_file):
    embedder = TransformerEmbedder(model_name, pooling='cls')
    indexer = LangChainIndex(embedder)

    indexed_docs = indexer.batch_train(input_file)
    faiss.write_index(indexer.faiss_index, output_file)

# Completion function that gets the answer using your Llama model
def create_chat_completion(question, context=None):
    prompt = f"Question: {question}"
    if context:
        prompt += f"\n\nContext: {context}"
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )
    return completion.choices[0]["message"]["content"].strip()

# Function for retrieving relevant passages using LangChain and generate answers using the Llama model
def question_answering(question, top_docs=3):
    indexer = LangChainIndex.load('faiss_index.idx', path_or_file=True)
    indexer.restore_documents('covid_qa_dataset.json', path_or_file=True)

    ranked_docs = indexer.search(question, k=top_docs)
    retrieved_contexts = [doc.text for doc in ranked_docs['documents']]

    best_answer = None
    best_score = float('-inf')

    for context in retrieved_contexts:
        answer = create_chat_completion(question, context).strip()
        score = indexer.embedder.score(answer, question)
        if score > best_score:
            best_answer = answer
            best_score = score

    return best_answer

# Fetch and process the COVID-QA dataset
process_covid_qa_dataset()

# Use 'distilbert-base-uncased' for the TransformerEmbedder and generate the Faiss index
model_name = 'distilbert-base-uncased'
generate_faiss_index('covid_qa_dataset.json', model_name, 'faiss_index.idx')

# Test the question-answering system
if __name__ == "__main__":
    question = "Can you tell me about the impacts of lockdowns during the COVID-19 pandemic?"
    answer = question_answering(question)
    print(f"Answer: {answer}")