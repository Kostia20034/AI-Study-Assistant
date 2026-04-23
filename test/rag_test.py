from rag import RAGPipeline

# initialize RAG
rag = RAGPipeline()

# add some test text
test_text = """
Backpropagation is an algorithm used to train neural networks.
It works by calculating the gradient of the loss function with respect to each weight.
The error signal flows backwards through the network from output to input.
Each weight gets nudged in the direction that reduces the error.

Gradient descent is an optimization algorithm.
It updates weights by moving in the direction of steepest descent.
Learning rate controls how big each step is.
Too high learning rate causes overshooting, too low causes slow training.

Neural networks consist of layers of neurons.
Each neuron applies a weighted sum followed by an activation function.
Deep networks have many hidden layers between input and output.
More layers allow learning more complex patterns.
"""

# add to RAG
rag.add_document(test_text, "ml_notes")

# search
query = "what is neuron layers?"
context = rag.get_context(query)

print(f"Query: {query}")
print(f"\nRelevant context found:")
print(context)