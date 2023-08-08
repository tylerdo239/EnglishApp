import transformers
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import requests
import json

# Define the maximum sequence length supported by the BERT model
max_seq_length = 512

# Initialize an empty list to store the rows that need to be added
rows_to_add = []

with open("data.json", "r") as json_file:
    data = json.load(json_file)

# # Get the number of rows in the 'data.json' file
# num_rows = len(data)
# print("Number of rows in data.json:", num_rows)

model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Replace the following variables with your Supabase URL and table name
supabase_url = "https://aolvcivgxwqcevttjter.supabase.co"
supabase_table = "documents"

# Define the Supabase API endpoint for updating the table
update_url = f"{supabase_url}/rest/v1/{supabase_table}"

# Define your Supabase API key (replace with your actual API key)
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvbHZjaXZneHdxY2V2dHRqdGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwMTI0NzksImV4cCI6MjAwMzU4ODQ3OX0.32tAdbaPI6RRIxFWz8vor-oJtTgZIwnRcV9bZYcPGCg"

# Set up the request headers with the API key
headers = {
    "apikey": api_key,
    "Content-Type": "application/json",
}

# Loop through each row in the JSON data
for row in data:
    # Extract the values from each column
    main_text = row["main"]
    question = row["question"]
    band = row["band"]
    coherence = row["coherence"]
    lexical = row["lexical"]

    # Combine all the text from different columns into a single input string
    # input_text = f"{main_text} {question} {band} {coherence} {lexical}"

    # Tokenize and preprocess the input text
    tokens = tokenizer(main_text, return_tensors="pt", truncation=True, max_length=max_seq_length)

    with torch.no_grad():
        # Generate embeddings (also known as word representations or features)
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state  # Extract embeddings from the model

    # Convert embeddings to a vector of length 1536
    embedding_data = embeddings.squeeze(0).mean(dim=0).cpu().numpy().tolist()
    if len(embedding_data) < 1536:
        padding_length = 1536 - len(embedding_data)
        embedding_data += [0] * padding_length
    elif len(embedding_data) > 1536:
        embedding_data = embedding_data[:1536]

    # Prepare the data for the row to be added
    new_row_data = {
        "main": main_text,
        "question": question,
        "band": band,
        "coherence": coherence,
        "lexical": lexical,
        "embedding": embedding_data,
    }

    # Append the row to the list for batch processing
    rows_to_add.append(new_row_data)

# Define the Supabase API endpoint for adding multiple rows
add_rows_url = f"{supabase_url}/rest/v1/{supabase_table}"

# Send the request to add the new rows to the Supabase table
response = requests.post(add_rows_url, headers=headers, json=rows_to_add)

# Check the response status
if response.status_code == 201:
    print("New rows have been successfully added to the table!")
else:
    print("Error occurred while adding the new rows to the table.")
    print(response.json())