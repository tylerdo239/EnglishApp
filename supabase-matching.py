import torch
from transformers import BertTokenizer, BertModel
import requests

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_embedding(text):
    # Tokenize and preprocess the input text
    tokens = tokenizer(text, return_tensors="pt")

    # Generate embeddings (also known as word representations or features)
    with torch.no_grad():
        outputs = model(**tokens)
        embeddings = outputs.last_hidden_state  # Extract embeddings from the model

    # Convert embeddings to a vector of length 1536
    embedding_data = embeddings.squeeze(0).mean(dim=0).cpu().numpy().tolist()
    if len(embedding_data) < 1536:
        padding_length = 1536 - len(embedding_data)
        embedding_data += [0] * padding_length
    elif len(embedding_data) > 1536:
        embedding_data = embedding_data[:1536]

    # Return the embedding vector
    return embedding_data

input_string = "Educational systems all around the world use formal examinations as a way of testing students' abilities and success rates. Although  it instils an unhealthy competitive sense among the students, it also has many benefits as examinations help in expressing our skillset. In my essay below, I will further discuss my opinion. Without examination, students might become lethargic and lose  interest to prove their skillset. Moreover, exams increase our creativity skills as we solve tough problems within a limited amount of time, and it teaches us how to handle pressure and difficult questions. Although it may sound fancy that just acquiring knowledge is enough,  one needs to express their knowledge and people should be able to quantify it. Hence, it makes sense that examinations are preferred in most countries to access a studentâ€™s ability. That being said, some people see exams with a competitive sense and they compare themselves with other people, which creates a sense of pressure to perform well among others. Such behaviours should be avoided because people might go into depression or other disorders when they fail their examinations badly. Hence, people should see examinations as a way of accessing oneâ€™s ability for their own development rather than seeing them as achievements.  In conclusion, although competitive exams create a lot of insecurity in  many people, it is most beneficial for oneâ€™s growth and I believe certainly its advantages outweigh the drawbacks. If we see examinations as a natural way of accessing oneâ€™s ability and getting rid of the unhealthy competitive sense and insecurities, we can improve our skillset to a greater extent, as, one can always try again and be better, and failures and success are not permanent.Submitted by hemaecengineer on Fri Jul 07 2023"
query_embedding = get_embedding(input_string)
print(query_embedding)

# Replace with your actual Supabase URL, table name, and API key
supabase_url = "https://aolvcivgxwqcevttjter.supabase.co"
supabase_table = "documents"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvbHZjaXZneHdxY2V2dHRqdGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODgwMTI0NzksImV4cCI6MjAwMzU4ODQ3OX0.32tAdbaPI6RRIxFWz8vor-oJtTgZIwnRcV9bZYcPGCg"

# Define the Supabase API endpoint for the match_documents function
match_documents_url = f"{supabase_url}/rpc/match_documents"

# Set up the request headers with the API key
headers = {
    "apikey": api_key,
    "Content-Type": "application/json",
}

# Prepare the data to be sent in the request body
data_to_send = {
    "query_embedding": query_embedding,
    "match_threshold": 0.1,  # Replace with your desired similarity threshold
    "match_count": 1,  # Replace with the maximum number of matching documents you want to retrieve
}

# Send the request to the match_documents function
response = requests.post(match_documents_url, headers=headers, json=data_to_send)

# Check the response status
if response.status_code == 200:
    matching_documents = response.json()
    print("Matching Documents:")
    print(matching_documents)
else:
    print("Error occurred while retrieving matching documents.")
    print(response.json())
