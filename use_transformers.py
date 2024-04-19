#pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer, util
sentences = ["write a story about rabbit","you are the summarizer. You can create concise and informative summaries."]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

cosine_similarity = util.pytorch_cos_sim(embedding_1, embedding_2)
print(cosine_similarity.item())
## tensor([[0.6003]])
