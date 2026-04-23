# training data for fine tuning
# format: list of conversations

training_data = [
    {
        "instruction": "What is a neural network?",
        "output": "A neural network is a collection of numbers organized in layers. Each number is called a weight. Data flows through layers of matrix multiplications, each one transforming the input into a richer representation. The network learns by adjusting these weights to minimize prediction errors."
    },
    {
        "instruction": "What is backpropagation?",
        "output": "Backpropagation is the algorithm that trains neural networks. After the network makes a prediction, we calculate how wrong it was. Then we flow that error signal backwards through every layer, calculating how much each weight contributed to the mistake. Finally we nudge every weight slightly in the direction that reduces the error."
    },
    {
        "instruction": "What is an embedding?",
        "output": "An embedding is a vector — a list of numbers that represents the meaning of a word or sentence. Similar meanings produce similar vectors. The word cat and the word dog would have vectors close together. The word pizza would be far away from both. Embeddings place meaning in mathematical space."
    },
    {
        "instruction": "What is RAG?",
        "output": "RAG stands for Retrieval Augmented Generation. Instead of relying only on training data, the model retrieves relevant chunks from a document database first. Then it generates an answer based on those retrieved chunks. This grounds the AI in real documents and reduces hallucination."
    },
    {
        "instruction": "What is a transformer?",
        "output": "A transformer is a neural network architecture that uses attention to process all tokens simultaneously instead of sequentially. The attention mechanism lets each token look at every other token and decide which ones are most relevant. This allows transformers to understand long range dependencies in text."
    },
    {
        "instruction": "What is fine tuning?",
        "output": "Fine tuning takes a pre-trained model and trains it further on specific data. The model already knows language from pre-training. Fine tuning teaches it new behavior or specialized knowledge on top of that foundation. It is much cheaper than training from scratch because most of the learning already happened."
    },
    {
        "instruction": "What is a token?",
        "output": "A token is a chunk of text that the model processes as one unit. Words get split into tokens based on frequency. Common words like the get one token. Rare words get split into multiple tokens. The model never sees raw text — only token IDs that map to vectors."
    },
    {
        "instruction": "What is gradient descent?",
        "output": "Gradient descent is the optimization algorithm that trains neural networks. After calculating how wrong the model was, we compute the gradient — which direction to adjust each weight to reduce the error. Then we take a small step in that direction. Repeat billions of times and the model learns."
    },
    {
        "instruction": "What is a context window?",
        "output": "The context window is the maximum amount of text a model can see at once. It is measured in tokens. Everything outside the context window is invisible to the model. For long conversations or large documents you must carefully manage what fits inside this limit."
    },
    {
        "instruction": "What is a vector database?",
        "output": "A vector database stores embeddings and searches by similarity. Instead of exact keyword matching like SQL, it finds vectors with similar meaning. When you search with a question it converts the question to a vector and finds the closest stored vectors. ChromaDB and Pinecone are examples."
    }
]

if __name__ == "__main__":
    print(f"Training examples: {len(training_data)}")
    for item in training_data:
        print(f"\nQ: {item['instruction']}")
        print(f"A: {item['output'][:100]}...")
