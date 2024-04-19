from tl_df import calculate_tfidf_vector, cosine_similarity

dic = {
   'story':
      {'role': "you are the storyteller. You can create new and creative stories.",
      'prompt': "{character} embarks on a {adjective} adventure in the {location}. As they {action}, unexpected {event} occurs, leading to a thrilling climax. How does {character} overcome the challenges and what is the resolution of this {genre} story?"},

   'song':
      {'role': "you are the songwriter. You can craft lyrics for various genres and themes.",
      'prompt': "Compose lyrics for a {genre} song titled '{title}'. The song should capture the essence of {emotion} and revolve around the theme of {theme}. Explore {element} and convey a message of {message}. How does the chorus resonate with the overall {mood} of the song?"},

   'summary':
      {'role': "you are the summarizer. You can create concise and informative summaries.",
      'prompt': "Generate a summary for the following {type} titled '{title}'. Provide a brief overview of the given {text} and mention any notable insights . Ensure the summary is around {length} words."},
   
   'youtube':
      {'role':"open youtube in browser",
      'prompt': "https://www.youtube.com"},
   
   'download_video':
      {'role':'download a youtube video from given link'},
   
   'instagram':
      {'role': "open instagram in browser",
      'prompt': "https://www.instagram.com"},
      
   'safari':
      {
         'role':"open safari browser",
         'prompt': "/Applications/safari.app"
      },
   'asphalt9':
      {
         'role': "open asphalt9 game",
         'prompt':"/Applications/Asphalt9.app"
      },
   'chess':
      {
         'role':"open chess game",
         'prompt': "/System/Applications/Chess.app"
      },
   'github':
      {
         'role':"open github website",
         'prompt': "https://github.com"
      },
   'youtube_trending':
      {
         'role':"open youtube trending page",
         'prompt': "https://www.youtube.com/feed/trending"
      },
   'youtube_search':
      {
         'role':"search on youtube website",
         'prompt':"https://www.youtube.com/results?search_query={search}"
      },
   'incognito_mode':
      {
         'role':"open safari in incognito mode"
      }
} 


def tl_df_similarity(prompt):
   all_data = [val['role'] for key, val in dic.items()]
   combined_data = [prompt]+all_data
   tfidf_matrix = [calculate_tfidf_vector(document, combined_data) for document in combined_data]
   
   target_vector = tfidf_matrix[0]
   new_data = {key: vec for key, vec in zip(dic.keys(), tfidf_matrix[1:])}
   maximum = float('-inf')
   content_type = None

   for key, vector in new_data.items():
      print(key , vector)
      similarity_score = cosine_similarity(target_vector, vector)
      # print(f"Cosine Similarity between Target and Document {i + 1}: {simi_scor
      if similarity_score > maximum:
            maximum = similarity_score
            content_type = key
   return key 


prompt = "hello how are you"
key = tl_df_similarity(prompt)
print(key)