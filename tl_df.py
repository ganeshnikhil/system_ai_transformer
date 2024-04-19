import math
from collections import Counter


def calculate_tf(word, document):
   return document.count(word) / len(document)


def calculate_idf(word, documents):
   num_documents_containing_word = sum(1 for document in documents if word in document)
   return math.log(len(documents) / (1 + num_documents_containing_word))


def calculate_tfidf(word, document, documents):
   tf = calculate_tf(word, document)
   idf = calculate_idf(word, documents)
   return tf * idf


def calculate_tfidf_vector(document, documents):
   unique_words = set(document.split())
   tfidf_vector = [calculate_tfidf(word, document, documents) for word in unique_words]
   return tfidf_vector


def cosine_similarity(vector1, vector2):
   dot_product = sum(a * b for a, b in zip(vector1, vector2))
   norm_vector1 = math.sqrt(sum(a ** 2 for a in vector1))
   norm_vector2 = math.sqrt(sum(b ** 2 for b in vector2))
   similarity = dot_product / (norm_vector1 * norm_vector2)
   return similarity
# Example data


def main():
   data = ["quick brown fox jumps over a lazy dog","the quick brown fox jumps over the lazy dog"]

# Target sentence
   target = "quick brown fox jumps over a lazy dog"

# Combine data and target for TF-IDF calculation
   combined_data = [target] + data

# Calculate TF-IDF vectors for each document
   tfidf_matrix = [calculate_tfidf_vector(document, combined_data) for document in combined_data]
   target_vector = tfidf_matrix[0]

   print(tfidf_matrix)
   print("\n")
   print(tfidf_matrix[1:])
   for i, vector in enumerate(tfidf_matrix[1:]):
      simi_score = cosine_similarity(target_vector, vector)
      print(f"Cosine Similarity between Target and Document {i + 1}: {simi_score}")


# Assuming you already have the TF-IDF matrix calculated as tfidf_matrix
# Using the scikit-learn example from above


# Function to calculate cosine similarity


# target_vector = tfidf_matrix[0]
# print(tfidf_matrix)
# print("\n")
# print(tfidf_matrix[1:])
# for i, vector in enumerate(tfidf_matrix[1:]):
#    simi_score = cosine_similarity(target_vector, vector)
#    print(f"Cosine Similarity between Target and Document {i + 1}: {simi_score}")
