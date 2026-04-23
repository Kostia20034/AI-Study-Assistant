import urllib.request
import json
import os

class AIPet:
    def __init__(self, name, subject):
        self.name = name
        self.subject = subject
        self.memory_file = f"{name}_{subject}_memory.json"
        
        # Safety check: if file exists and isn't empty, load it
        if os.path.exists(self.memory_file) and os.path.getsize(self.memory_file) > 0:
            try:
                with open(self.memory_file, "r") as f:
                    self.messages = json.load(f)
                print(f"🧠 {name} remembers your previous session!")
            except:
                self.messages = self._get_default_system_prompt()
        else:
            self.messages = self._get_default_system_prompt()
            print(f"🐾 {name} is starting fresh!")

    def _get_default_system_prompt(self):
        return [
            {
                "role": "system",
                "content": f"You are {self.name}, an AI study assistant specializing in {self.subject}. Help students understand concepts clearly."
            }
        ]

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.messages, f)

    def chat(self, user_message, base64_image=None):
        # Create the message object
        new_message = {"role": "user", "content": user_message}
        
        # Only attach images if they exist
        if base64_image:
            new_message["images"] = [base64_image]

        self.messages.append(new_message)

        # Prepare payload for Ollama
        data = json.dumps({
            "model": "llama3.2",
            "messages": self.messages,
            "stream": False
        }).encode('utf-8')

        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                ai_response = result['message']['content']

            self.messages.append({"role": "assistant", "content": ai_response})
            self.save_memory()
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}. Make sure 'ollama pull llama3.2-vision' was run."

    def quiz_me(self):
        return self.chat(f"Generate 3 practice questions about {self.subject}.")