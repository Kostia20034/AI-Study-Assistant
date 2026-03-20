import urllib.request
import json
import os #add output stream
# initialize class
class AIPet:
  # constructor used for initialization of the obj
    def __init__(self, name, subject):
      # obj fields are just a map under the hood
        self.name = name
        self.subject = subject
        self.memory_file = f"{name}_{subject}_memory.json"
        if os.path.exists(self.memory_file):
          with open(self.memory_file, "r") as f:
            self.messages = json.load(f)
          print(f"🧠 {name} remembers your previous session!")
        else:
            # fresh start
            self.messages = [
                {
                    "role": "system",
                    "content": f"You are {name}, an AI study assistant that specializes in {subject}. You help students understand concepts, generate practice problems, and prepare for interviews and exams. Keep answers clear and educational."
                }
            ]
            print(f"🐾 {name} is starting fresh!")
            
    def save_memory(self):
        with open(self.memory_file, "w") as f:
          json.dump(self.messages, f)
      # ask chat a question +
      # 1) append your message
      # 2) convert to bytes
      # 3) create requst
      # 4) grab and save server response
      # 5) return ai's response
    def chat(self, user_message):
        # add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # send full conversation to ollama
        # map -> json -> bytes
        data = json.dumps({
            "model": "llama3.2",
            "messages": self.messages,
            "stream": False
        }).encode('utf-8')
        # send request to the server(olama)
        req = urllib.request.Request(
            "http://localhost:11434/api/chat", #url
            data=data, # get data 
            headers={"Content-Type": "application/json"} #hz general shit
        )
        # open req as stream with response name
        # convert bytes->json->map with name result
        # with is opening string as {name}
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            ai_response = result['message']['content']

        # remember ai response for next message
        self.messages.append({
            "role": "assistant",
            "content": ai_response
        })
        self.save_memory()
        return ai_response

    def quiz_me(self):
        return self.chat(f"Generate 3 practice questions about {self.subject}. Number them 1, 2, 3.")

    def show_history(self):
        for msg in self.messages:
            if msg["role"] != "system":
                print(f"\n{msg['role'].upper()}: {msg['content']}")


# run it
pet = AIPet("Nova", "Python")

print(f"🐾 {pet.name} is ready and is expert in {pet.subject} subject \n")
print("Type 'quit' to exit, 'quiz' to get practice questions\n")

while True:
  userinput = input("You: ")
  
  if userinput == "quit":
    print("Bye\n")
    break
  
  if userinput == "quiz":
    response = pet.quiz_me()

  else:
    response = pet.chat(userinput)
  
  print(f"\nNova: {response}\n")