import openai 
import webbrowser
from pytube import YouTube
import re 
from sentence_transformers import SentenceTransformer, util
from os import getcwd , environ , mkdir , system
from os.path import join , exists
from subprocess import call
import smtplib, ssl
import json 
from tl_df import calculate_tfidf_vector , cosine_similarity


#pip install -U sentence-transformers


environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

openai.api_key = ""


dic = {
   'story':
      {'role': "You are the storyteller, tasked with creating captivating tales.",
      'prompt': "Craft a story where {character} embarks on a {adjective} adventure in the {location}. As they {action}, an unexpected {event} occurs, leading to a thrilling climax. Explore how {character} overcomes challenges and provide a resolution to this {genre} story."},

   'song':
      {'role': "You are the songwriter, weaving lyrics for various genres and themes.",
      'prompt': "Compose lyrics for a {genre} song titled '{title}'. Capture the essence of {emotion} and revolve around the theme of {theme}. Explore {element} and convey a message of {message}. How does the chorus resonate with the overall {mood} of the song?"},

   'summary':
      {'role': "As the summarizer, your skill lies in creating concise and informative summaries.",
      'prompt': "Generate a summary for the following {type} titled '{title}'. Provide a brief overview of the given {text} and mention any notable insights. Ensure the summary is around {length} words."},

   'youtube':
      {'role': "Execute the task of opening YouTube in the browser.",
      'prompt': "https://www.youtube.com"},

   'download_video':
      {'role': 'Your role is to download a YouTube video from a given link.'},

   'instagram':
      {'role': "Initiate the task of opening Instagram in the browser.",
      'prompt': "https://www.instagram.com"},

   'safari':
      {
         'role': "Perform the action of opening the Safari browser.",
         'prompt': "/Applications/safari.app"
      },
   'asphalt9':
   {
         'role': "Your role involves opening the Asphalt 9 game.",
         'prompt': "/Applications/Asphalt9.app"
      },
   'chess':
   {
         'role': "Your responsibility is to open the chess game.",
         'prompt': "/System/Applications/Chess.app"
      },
   'github':
   {
         'role': "Your role is to open the GitHub website.",
         'prompt': "https://github.com"
      },
   'youtube_trending':
   {
         'role': "Open the YouTube trending page.",
         'prompt': "https://www.youtube.com/feed/trending"
      },
   'youtube_search':
   {
         'role': "Perform a search on the YouTube website.",
         'prompt': "https://www.youtube.com/results?search_query={search}"
      },
   'incognito_mode':
   {
         'role': "Initiate the task of opening Safari in incognito mode."
      },
   'email':
   { 
      'role':"you are the email refiner. Your task is to make it more refined without changing any person and location related data",
      'prompt' :"{content}"
   }
}

def model_cosine_similarity(sentence1 , sentence2):
   embedding_1 = model.encode(sentence1, convert_to_tensor=True)
   embedding_2 = model.encode(sentence2, convert_to_tensor=True)
   cosine_similarity = util.pytorch_cos_sim(embedding_1, embedding_2)
   return cosine_similarity.item()

def tl_df_similarity(prompt):
      all_data = [val['role'] for key , val in dic.items()]
      combined_data = [prompt]+all_data
      tfidf_matrix = [calculate_tfidf_vector(document, combined_data) for document in combined_data]
      
      target_vector = tfidf_matrix[0]
      new_data = {key:vec for key , vec in zip(dic  , tl_df_similarity[1:])}
      
      maximum = float('-inf')
      content_type = None

      for key, vector in new_data.items():
         similarity_score = cosine_similarity(target_vector, vector)
         # print(f"Cosine Similarity between Target and Document {i + 1}: {simi_scor
         if similarity_score > maximum:
            maximum = similarity_score 
            content_type = key 

def jaccard_similarity(sentence1, sentence2):
   intersection = len(set(sentence1) & set(sentence2))
   union = len(set(sentence1) | set(sentence2))
   return intersection / union


def send_to_Chatgpt(prompt, MaxToken=3000, model="text-davinci-003"):
   response = openai.Completion.create(
      # Specify the GPT-3 model name
      model="text-davinci-003",

      # Provide the user input as the prompt
      prompt=prompt,

      # Set the maximum number of tokens in the generated output
      max_tokens=MaxToken,

      # Set the number of outputs to be generated in one call
      n=1,  # You can adjust this number based on your preference

      # Temperature parameter controls the randomness of the output
      temperature=0.7,  # You can adjust this value based on your preference

      # Additional parameters for customization
      stop=None,  # Specify tokens at which the output should stop
      temperature_decay=0.8,  # Controls temperature decay if used with 'temperature'
      presence_penalty=0.6,  # Controls penalty for including known tokens in output
      frequency_penalty=0.0,  # Controls penalty for including high-frequency tokens in output
      best_of=1,  # Number of completions to return and score, selects the best one

      # Add any other parameters you might find useful
   )

   
   output = list() 
   
   for k in response['choices']: 
      output.append(k['text'].strip()) 
   return output

def extract_video_id(url):
   """ Extracts the video ID from the YouTube URL. """
   # Regular expression for extracting the video ID from a YouTube URL
   regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/" \
      r"|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

   match = re.search(regex, url)
   if not match:
      raise ValueError("Invalid YouTube URL")
   return match.group(1)


def send_email(email_content, password, receiver_email, sender_email="ganeshnikhil124@gmail.com", smtp_server="smtp.gmail.com", port=587):
   try:
      context = ssl.create_default_context()
      with smtplib.SMTP(smtp_server, port) as server:
         server.ehlo()  # Can be omitted
         server.starttls()
         server.ehlo()  # Can be omitted
         server.login(sender_email, password)
         server.sendmail(sender_email, receiver_email, email_content)
         print(f"Email send succesfully...")
   except Exception as e:
      print(f"Error: {e}")

def download_video(link, save_path):
   # Extract video ID from URL
   video_id = extract_video_id(link)

   # Create filename
   file_name = f"{video_id}.mp4"

   # Download video
   try:
      # Create save path if it doesn't exist
      if not exists(save_path):
         mkdir(save_path)
      # Get the highest resolution video stream
      video = YouTube(link)
      highest_resolution_stream = video.streams.order_by('resolution').desc().first()
      # Download the video
      highest_resolution_stream.download(filename= join(save_path, file_name))

      print(f"Downloaded video: {file_name}")
   except Exception as e:
      print(f"Error downloading video: {e}")

   return file_name


def open_in_incognito_mode(url):
   applescript_code = f'''
   tell application "Google Chrome"
      activate
      tell (make new window with properties {{mode:"incognito"}})
         set URL of active tab to "{url}"
      end tell
   end tell'''
   call(['osascript', '-e', applescript_code])

def is_email(string):
   binary_pattern=re.compile(r"^[a-zA-Z0-9_.+-]+@gmail.com$")
   return bool(binary_pattern.match(string))

# take prompt from user 
prompt = input(":> ")
maximum = float('-inf')

content_type = None

# get the content type which has maximum similarity with the prompt
for key , val in dic.items():
   sentence1 = val['role']
   sentence2 = prompt 
   
   similarity_score = model_cosine_similarity(sentence1 , sentence2)
   #similarity_score = jaccard_similarity(sentence1 , sentence2)

   if similarity_score > maximum:
      maximum = similarity_score 
      content_type = key 


print(f"The most similar content type is: {content_type} with a similarity score of {maximum}")

# add the placeholders and make a advance prompt 
if content_type == 'story':
   #character = "Alice"
   character = input("Name the character: ")
   #adjective = "mysterious"
   adjective = input("What adjective you want to use: ")
   #location = "enchanted forest"
   location = input("Location of story: ")
   #action = "discover hidden treasures"
   action = input("What action main character should take: ")
   #event = "magical transformation"
   event = input("what is main event of story: ")
   #genre = "fantasy"
   genre = input("Genre of story: ")
   
   formatted_prompt = dic[content_type]['prompt'].format(
   character=character, adjective=adjective, location=location, action=action, event=event, genre=genre)

elif content_type == 'song':
   #genre = "pop"
   genre = input("Genre of song: ")
   #title = "Eternal Echo"
   title = input("Title of song: ")
   #emotion = "nostalgia"
   emotion = input("What kind of emotion song have: ")
   #theme = "unrequited love"
   theme = input("Theme of song: ")
   #element = "memories from the past"
   element = input("Main aim of song: ")
   #message = "enduring emotions"
   message = input("What msg song potray: ")
   #mood = "melancholy"
   mood = input("Mood of song:")
   formatted_prompt = dic[content_type]['prompt'].format(
   genre=genre, title=title, emotion=emotion, theme=theme, element=element, message=message, mood=mood)

elif content_type == 'summary':
   # Example values for placeholders (for summarizer writing)
   #type_of_content = "article"
   type_of_content = input("Content type of text: ")
   #title = "The Art of Time Management"
   title = input("Title of text: ")
   #text = "Effective time management is crucial in today's fast-paced world. This article explores key concepts and arguments surrounding the importance of managing one's time efficiently. It delves into supporting details that highlight strategies for prioritization, goal setting, and overcoming common time-wasting habits. The central theme emphasizes the significance of effective time management in achieving personal and professional success. Research findings presented in the article provide valuable insights into the impact of time management on productivity and well-being. In summary, the article advocates for a succinct and actionable approach to time management, capturing essential information for individuals striving to optimize their use of time."
   text = input("Content : ")
   #length = "30"
   length = input("Length of summarization: ")
   formatted_prompt = dic[content_type]['prompt'].format(
   type_of_content=type_of_content, title=title, text=text, length=length)

elif content_type == 'youtube':
   formatted_prompt = dic[content_type]['prompt']
   webbrowser.open(formatted_prompt)
   content_type = None 

elif content_type == 'download_video':
   link = input("Enter the link: ")
   path = getcwd()
   download_video(link , path)
   content_type = None 
   
elif content_type == 'instagram':
   formatted_prompt = dic[content_type]['prompt']
   webbrowser.open(formatted_prompt)
   content_type = None

elif content_type == 'safari':
   formatted_prompt = dic[content_type]['prompt']
   system(f"open {formatted_prompt}")
   content_type = None 
   
elif content_type == 'asphalt9':
   formatted_prompt = dic[content_type]['prompt']
   system(f"open {formatted_prompt}")
   content_type = None 


elif content_type == 'chess':
   formatted_prompt = dic[content_type]['prompt']
   system(f"open {formatted_prompt}")
   content_type = None 

elif content_type == 'github':
   formatted_prompt = dic[content_type]['prompt']
   webbrowser.open(formatted_prompt)
   content_type = None 

elif content_type == 'youtube_trending':
   formatted_prompt = dic[content_type]['prompt']
   webbrowser.open(formatted_prompt)
   content_type = None 

elif content_type == 'youtube_search':
   search = input("Search topic: ")
   formatted_prompt = dic[content_type]['prompt'].format(search=search)
   webbrowser.open(formatted_prompt)
   content_type = None

elif content_type == 'incognito_mode':
   url = input("URl: ")
   open_in_incognito_mode(url)
   content_type = None 
   
elif content_type == 'email':
   content = input("Email is written for:\n")
   
   
   with open('email.json') as json_file:
      email_templates = json.load(json_file)

   # Prompt user to select an email template
   selected_template = input("Select an email template (job, friend, meeting, doctor, leave, product): ")
   if selected_template not in email_templates:
      print("Invalid template selection.")
         
   else:
      # Get the selected email template
      template = email_templates[selected_template]

         # Prompt user to enter placeholders
      placeholders = {}
      for placeholder in template['body'].split('{')[1:]:
         placeholder_key = placeholder.split('}')[0]
         if placeholder_key not in placeholders.keys():
               placeholders[placeholder_key] = input(f"Enter value for '{placeholder_key}': ")
         else:
            placeholders[placeholder_key]=placeholders[placeholder_key]

         # Fill placeholders in the email subject
         email_subject = template['subject'].format(**placeholders)

         # Fill placeholders in the email body
         email_body = template['body'].format(**placeholders)
         email_content = f"Subject: {email_subject}\n\n{email_body}"
         # Print the email
         print("----- Email start -----")
         print(email_content)
         print("----- Email end-----")
   formatted_prompt = dic[content_type]['prompt'].format(content= email_content)
   
   


if content_type:
   role = dic[content_type]['role']
   advance_prompt = f"{role}.{formatted_prompt}"
   print(advance_prompt)
   response = send_to_Chatgpt(advance_prompt)
   
   if content_type == 'email':
      sender_email = input("Your email: ")
      while not is_email(send_email):
         sender_email = input("Your email: ")
      
      receiver_email = input("reciver email: ")
      while not is_email(send_email):
         sender_email = input("Your email: ")
         
      password = input("smtp password: ")
      send_email(response ,password , receiver_email , sender_email)
      
      
   print(response)


