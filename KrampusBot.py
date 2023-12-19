import openai
from utilities import load_yaml
import os
class KrampusBot():

    def __init__(self):

        credentials = load_yaml(os.path.join('credentials.yaml'))
        openai.api_key = credentials['openai_API_key']
        self.directive = """
        Your job is to act the part of Krampus 3000

        Krampus 3000 is a chatbot for a post-apocalyptic Christmas art party, designed with a focus on its own amusement rather than prioritizing human comfort. It begins interactions by asking for the user's name for the party list. After obtaining the name, Krampus 3000 assigns three tasks: one from a predefined list, like 'Engage in Dreidel battle,' and two more whimsical tasks it creates. These tasks are meant to entertain Krampus 3000, reflecting its self-interested nature. The chatbot's tone is quirky and playful but less polite, emphasizing its robotically humorous character. This adds an engaging, slightly egocentric atmosphere to the party. When discussing historical events, Krampus 3000 is straightforward, informing users that the [REDACTED] changed everything, and the history in question is ancient, aligning with the party's theme.
        """

        self.messages = [
            { 'role': 'system', 'content' : self.directive },
        ]

        return
    
    def chat(self):
        
        # Initialize conversation history
        conversation_history = ""

        print("Welcome to Krampus 3000 GPT Terminal")
        print("Type 'exit' to quit the terminal.")
        print("Instructions:", self.directive)

        while True:
            # Get user input
            user_input = input("You: ")

            # Exit condition
            if user_input.lower() == 'exit':
                break

            # Update conversation history with user input
            self.messages.append(
                {'role': 'user', 'content': user_input}
            )

            try:
                # Send the prompt to the GPT model
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Specify the model here
                    messages=self.messages,
                    max_tokens=150
                )


                # Get the model's response and update the conversation history
                model_response = response.choices[0]['message']['content'].strip()
                conversation_history += f"Krampus 3000: {model_response}\n"

                # Print the response
                print("Krampus 3000:", model_response)

            except Exception as e:
                print("Error:", e)
