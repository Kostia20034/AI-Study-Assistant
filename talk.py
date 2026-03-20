import urllib.request
import json

# def chat(message):
#     data = json.dumps({
#         "model": "llama3.2",
#         "messages": [{"role": "user", "content": message}],
#         "stream": False
#     }).encode('utf-8')

#     req = urllib.request.Request(
#         "http://localhost:11434/api/chat",
#         data=data,
#         headers={"Content-Type": "application/json"}
#     )

#     with urllib.request.urlopen(req) as response:
#         result = json.loads(response.read().decode('utf-8'))
#         return result['message']['content']

# response = chat("explain what a neural network is in 3 sentences")
# print(response)
# ```

# Then open terminal in VS Code (Ctrl + `) and run:
# ```
# python talk.py
def addition(a, b):
  return a + b

# x = 5
# name = "John"
# print(name)
# print(addition(5,6))

# store = {
#   "banana" : 10,
#   "sliva" : 15,
#   "kavun" : 20
# }

# print(store["banana"])
# print(store["sliva"])

list = ["kavun","dynia", "ogirok"]

# print(list[0])
# print(list[-1])
# print(list[-2])
# print(list[2])

name = "kostia"
age = 23
print(f"My name is {name} i am {age} years old")

# for item in list:
#   print(item)

i = 0
while i < 3:
    print(list[i])
    i += 1
