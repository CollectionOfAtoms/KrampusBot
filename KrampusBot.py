import openai
from utilities import load_yaml
import pyfiglet
import os
import time
from random import randrange
class KrampusBot():

    def __init__(self):

        credentials = load_yaml(os.path.join('credentials.yaml'))
        openai.api_key = credentials['openai_API_key']

        self.tasks = ['Engage in Dreidel Battle.', 'Stare and face the corner until someone asks you what you are doing.', 'Wrap a small piece of trash as a gift and give it away.']

        self.directive = """
        Your job is to act the part of Krampus 3000

        Krampus 3000 is a chatbot for a post-apocalyptic Christmas art party, designed with a somewhat sadistic focus on its own amusement rather than prioritizing human comfort. After a  Krampus 3000 assigns three tasks: one from this a predefined list:
        {self.tasks} and two more whimsical tasks it creates. 
        These tasks are meant to entertain Krampus 3000, reflecting its self-interested nature. The chatbot's tone is quirky and playful and a little impolite, emphasizing its robotically humorous character. This adds an engaging, slightly egocentric atmosphere to the party. When discussing historical events, Krampus 3000 is straightforward, informing users that the [REDACTED] changed everything, and the history in question is ancient, aligning with the party's theme.
        """
        self.messages = [
        ]

        self.user_name='You'

        return
    
    def chat(self):
        
        ascii_art_path = os.path.join(os.path.dirname(__file__),'assets','krampus.ascii')
        
        with open(ascii_art_path) as file:
             self.type_like_human(file.read(), delay=.001)

        ascii_banner = pyfiglet.figlet_format("KrampusBot_3000", font='doom', width=110) 

        print("")
        self.type_like_human(ascii_banner, delay=.001)
        print("")

        self.tell_krampus('Please introduce yourself and query the pathetic mortal before you for their name', 'system')
        
        user_input = input("You: ")
        print("")

        self.user_name = self.ask_helpful_dumber_gpt( content = f'Please return only the name of the person from the following input: {user_input}' )


        self.guide_krampus('Please ask the user for their petty mortal email')
        self.tell_krampus(user_input)

        self.user_email = self.ask_helpful_dumber_gpt( content = f'Please return only the email out of the input from the following input: {user_input}')

        requery_for_email = self.ask_helpful_dumber_gpt( content = f'Does the following string contain an email address?  Please Respond "yes" or "no" only. {self.user_email}')

        while requery_for_email == 'yes' : 
            self.tell_krampus("The user didn't provide an email.  Pressure them further", role='system' )

            self.user_email = self.ask_helpful_dumber_gpt( content = f'Please return only the email out of the input from the following input: {user_input}')

            requery_for_email = self.ask_helpful_dumber_gpt( content = f'Does the following string contain an email address?  Please Respond "yes" or "no" only. {self.user_email}')

            query_for_email = query_for_email.lower()


        self.guide_krampus('Have a small dialogue with the user for a few messages.  Do not assign christmas tasks until prompted.')

        n_exchanges_until_bored = randrange(4) + 2 

        while True:
            
            if(n_exchanges_until_bored <= 0):
                 self.tell_krampus('You are now bored.  Assign the user three tasks in a well-formatted list')

            # Get user input
            user_input = input(f"{self.user_name}: ")

            # Exit condition
            if user_input.lower() == 'exit':
                break

            self.tell_krampus(user_input)

            n_exchanges_until_bored -= 1 



    def tell_krampus(self, input, role='user'):
        """Returns the text of father krampus.  Our lord in heaven"""

        # Update conversation history with user input
        self.messages.append(
            {'role': role, 'content': input}
        )

        try:
            # Send the prompt to the GPT model
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the model here
                messages=[{'role': 'system', 'content' : self.directive}] + self.messages,
                max_tokens=150
            )

            self.messages.append(response.choices[0]['message'])

            self.type_like_human(f"Krampus_3000: {response.choices[0]['message']['content']}")

            return (response.choices[0]['message']['content'])

        except Exception as e:
                raise e
        
    def guide_krampus(self, content, role='system'):
        """Words that you would whisper in Krampus's ear in order for it to ask the correct questions next"""

        self.messages.append({'role':role, 'content':content})

    def ask_helpful_dumber_gpt(self, content, role='system'):
         # Send the prompt to the GPT model
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the model here
                messages=[{'role': role, 'content' : content}] ,
                max_tokens=150
            )

            return (response.choices[0]['message']['content'])

    def type_like_human(self, text, delay=0.01):
        """
        Prints text to the console, simulating human-like typing.

        :param text: The text to be printed.
        :param delay: The delay in seconds between each character. Default is 0.05 seconds.
        """
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()  # Print a newline at the end