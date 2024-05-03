import openai

# Set the API key and API base URL for OpenAI
openai.api_key = "EMPTY"
openai.api_base = "https://api.llm.lab.epam.com/v1"

# Set the model name you want to use for the requests
model = "Llama-2-70B-chat-AWQ"

def divider(length: int = 40):
    print('-' * length)

def create_completion(prompt):
    # The Completion API creates a text snippet based on a given prompt.
    # Here, we pass the model, prompt text, and the maximum number of tokens
    # to generate in the response.
    completion = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=80
    )
    # Print the generated output
    print(completion.choices[0].text.strip())
    divider()

def create_chat_completion(message):
    # The Chat Completion API creates a message-based conversation snippet.
    # It takes a series of input messages (including a user message in this example)
    # and generates a response based on the provided context.
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        max_tokens=80
    )
    # Print the generated output
    print(completion.choices[0]['message']['content'].strip())
    divider()


def simple_testing():
    # Test the 'create_completion' API
    # In the function call, we provide a prompt related to generating a Python
    # function that adds two numbers. The LLM will generate a completion based
    # on the given prompt.
    create_completion("Write a python function that adds two numbers")

    # Test the 'create_chat_completion' API
    # In this function call, we provide a user message asking about the best
    # food in Paris. The LLM will generate a conversation snippet based on the
    # provided message.
    create_chat_completion("What is the best food in Paris?")


def conversational_repl_no_memory():
    print("Starting conversational REPL. Enter an empty line to exit.")
    while True:
        user_message = input("User: ")
        if not user_message:
            print("System: Thank you for chatting! Have a great day!")
            break
        create_chat_completion(user_message)


def conversational_repl_with_memory():
    print("Starting conversational REPL. Enter special commands with '/', like '/RESET', '/SET_MIN_TOKENS' or '/SET_TOKENS_PER_MESSAGE'. Enter an empty line to exit.")
    
    messages = []
    MIN_TOKENS = 80
    TOKENS_PER_MESSAGE = 20

    while True:
        divider()
        user_message = input("User: ")

        # Handle special commands with '/'
        if user_message.startswith('/'):
            command = user_message.upper()

            if command == "/RESET":
                messages = []
                print("System: Conversation reset.")
                continue
            elif command == "/SET_MIN_TOKENS":
                try:
                    new_value = int(input("System: Enter the new MIN_TOKENS value: "))
                    MIN_TOKENS = new_value
                    print(f"System: MIN_TOKENS set to {MIN_TOKENS}")
                except ValueError:
                    print("System: Invalid value for MIN_TOKENS.")
                continue
            elif command == "/SET_TOKENS_PER_MESSAGE":
                try:
                    new_value = int(input("System: Enter the new TOKENS_PER_MESSAGE value: "))
                    TOKENS_PER_MESSAGE = new_value
                    print(f"System: TOKENS_PER_MESSAGE set to {TOKENS_PER_MESSAGE}")
                except ValueError:
                    print("System: Invalid value for TOKENS_PER_MESSAGE.")
                continue
            else:
                print("System: Unknown command.")
                continue

        # Check when the user enters empty input
        if not user_message:
            print("System: Thank you for chatting! Have a great day!")
            break

        # Add the user message to the list of messages
        messages.append({"role": "user", "content": user_message})

        # Calculate tokens dynamically based on message count
        max_tokens = max(MIN_TOKENS, len(messages) * TOKENS_PER_MESSAGE)

        # Get the chat completion response
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        # Get the generated output
        system_response = completion.choices[0]['message']['content'].strip()

        # Add the system message to the list of messages
        messages.append({"role": "system", "content": system_response})

        print(f"System: {system_response}")


def conversational_repl():
    """Interactive loop for prompt reading and response, with memory"""

    divider()

    print("Starting conversational REPL. Enter special commands with '/', like '/RESET', '/SET_MIN_TOKENS' or '/SET_TOKENS_PER_MESSAGE'. Enter an empty line to exit.")
    
    messages = []
    MIN_TOKENS = 80
    TOKENS_PER_MESSAGE = 20

    while True:
        divider()
        user_message = input("User: ")
        
        # ... handling '/', RESET, SET_MIN_TOKENS, SET_TOKENS_PER_MESSAGE ...

        if not user_message:
            print("System: Thank you for chatting! Have a great day!")
            break

        messages.append({"role": "user", "content": user_message})

        conversation_length = sum(len(msg['content']) for msg in messages)
        input_length = len(user_message)
        
        # Adjust available space out of total model limit, leaving buffer for the remaining tokens
        buffer_space = 10  # Arbitrary buffer space to avoid reaching the token limit
        total_model_limit = 4096  # Set this to the specific LLM model limit you're using, e.g., 4096 for gpt-3.5-turbo
        available_space = total_model_limit - (conversation_length + input_length) - buffer_space
        
        if available_space <= 0:
            print("System: Conversation reached token limit. Please reset the conversation or trim the history.")
            break

        max_tokens = min(max(MIN_TOKENS, len(messages) * TOKENS_PER_MESSAGE), available_space)

        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        system_response = completion.choices[0]['message']['content'].strip()

        messages.append({"role": "system", "content": system_response})

        print(f"System: {system_response}")

if __name__ == "__main__":
    # simple_testing()  # You can comment this line if you don't want to run the simple tests
    conversational_repl()
