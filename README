# Automated Data Query and Retrieval System

## Overview

This project implements an Automated Data Query and Retrieval System using:

- MongoDB
- Ollama (Offline Open Source LLM)
- LangChain
- LlamaIndex
- Python
- CSV Data

The system loads data from a CSV file into MongoDB, accepts natural language queries from the user, uses an offline Large Language Model to generate MongoDB queries, executes those queries, and displays or saves the results.

---

## Project Structure

AIQoD_Assignment/

├── main.py

├── config.py

├── database.py

├── llm.py

├── output_utils.py

├── sample_data.csv

├── Queries_generated.txt

├── .env

└── output/

  ├── test_case1.csv

  ├── test_case2.csv

  └── test_case3.csv

---

## Technologies Used

- Python
- MongoDB
- Ollama
- LangChain
- LlamaIndex
- Pandas
- PyMongo

---

## Setup Instructions

### 1. Install MongoDB

Download and install MongoDB Community Server.

Verify installation:

mongod --version

---

### 2. Start MongoDB

Windows:

net start MongoDB

---

### 3. Install Ollama

Download and install Ollama.

Pull the model:

ollama pull llama3.2

Verify:

ollama list

---

### 4. Create Virtual Environment

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

---

### 5. Install Dependencies

pip install pandas pymongo python-dotenv

pip install langchain-core langchain-ollama

pip install llama-index

pip install llama-index-llms-ollama

pip install llama-index-embeddings-huggingface

pip install sentence-transformers

---

### 6. Create .env File

MONGO_URI=mongodb://localhost:27017/

OLLAMA_MODEL=llama3.2

---

### 7. Run Project

python main.py

---

## Workflow

1. CSV data is loaded into MongoDB.
2. LlamaIndex creates a semantic index over the CSV data.
3. User enters a natural language query.
4. LangChain constructs a prompt.
5. Ollama generates a MongoDB query.
6. MongoDB executes the query.
7. Results are displayed or saved as CSV.
8. Generated queries are logged in Queries_generated.txt.

---

## Test Cases

### Test Case 1

Find all products with a rating below 4.5 that have more than 200 reviews and are offered by the brand Nike or Sony.

Output File:

test_case1.csv

---

### Test Case 2

Which products in the Electronics category have a rating of 4.5 or higher and are in stock?

Output File:

test_case2.csv

---

### Test Case 3

List products launched after January 1, 2022, in the Home & Kitchen or Sports categories with a discount of 10% or more, sorted by price in descending order.

Output File:

test_case3.csv

---

## Features

- Offline LLM using Ollama
- Natural Language Querying
- MongoDB Query Generation
- Semantic Retrieval using LlamaIndex
- CSV Export
- Query Logging
- Input Validation
- MongoDB Indexing for Performance

---

## Output Files

- test_case1.csv
- test_case2.csv
- test_case3.csv
- Queries_generated.txt

These files are generated automatically when test cases are executed.
