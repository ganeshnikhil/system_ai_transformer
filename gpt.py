import pyttsx3
import openai
# "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"
openai.api_key = "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"

# function to convert text to speech


def speakText(command):
   engine = pyttsx3.init()
   engine.say(command)
   engine.runAndWait()



start = True
def send_to_Chatgpt(prompt, model="gpt-3.5-turbo"):
   response = openai.ChatCompletion.create(
      model=model,
      message=prompt,
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
   )
   message = response.choices[0].message.content
   messages.append(response.choices[0].message)
   return messages


messages = [
   {"role": "user", "content": "please act like jarvis from the iron man."}]
new_start = True
while new_start:
   text = input("Enter the input:")
   messages.append({"role": "user", "content": text})
   response = send_to_Chatgpt(messages)
   speakText(response)

   print(response)

 
