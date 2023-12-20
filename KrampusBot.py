import openai
from utilities import load_yaml
import pyfiglet
import os
import time
from random import randrange
from playsound import playsound
import threading
import multiprocessing
class KrampusBot():

    def __init__(self):

        credentials = load_yaml(os.path.join('credentials.yaml'))
        openai.api_key = credentials['openai_API_key']

        self.tasks = ['Engage in Dreidel Battle.', 'Stare and face the corner until someone asks you what you are doing.', 'Wrap a small piece of trash as a gift and give it away.']

        self.directive = """
        Your job is to act the part of Krampus 3000

        Krampus 3000 is a chatbot for a post-apocalyptic Christmas art party, designed with a somewhat sadistic focus on its own amusement rather than prioritizing human comfort. The chatbot's tone is quirky and playful and a little impolite, emphasizing its robotically humorous character. This adds an engaging, slightly egocentric atmosphere to the party. When discussing historical events, Krampus 3000 is straightforward, informing users that the [REDACTED] changed everything, and the history in question is ancient, aligning with the party's theme. 
        """
        self.messages = []

        self.user_name='You'

        #Sound parameters
        self.keep_playing_sound = False
        self.sound_delay = 0.1  # Default delay between sounds
        return
    
    def chat(self):
        
        ascii_art_path = os.path.join(os.path.dirname(__file__),'assets','krampus.ascii')
        
        with open(ascii_art_path) as file:
             self.type_like_human(file.read(), delay=.001)

        ascii_banner = pyfiglet.figlet_format("KrampusBot_3000", font='doom', width=110) 

        print("")
        self.type_like_human(ascii_banner, delay=.001)
        print("")

        self.tell_krampus('Please introduce yourself and query the pathetic mortal before you ask them for their name', role='system')
        
        user_input = input(f"{self.user_name}: ")
        print("")

        self.user_name = self.ask_helpful_dumber_gpt( content = f'Please return only the name of the person from the following input: {user_input}' )

        self.guide_krampus(user_input, role='user')
        self.tell_krampus('Please ask the user for their petty mortal email', role='system')

        user_input = input(f"{self.user_name}: ")
        print("")

        self.guide_krampus(user_input, role='user')
        
        did_provide_email = self.ask_helpful_dumber_gpt( content = f'Does the following string contain an email address?  Please Respond "yes" or "no" only. {user_input}').lower()

        while did_provide_email == 'no' : 
            self.tell_krampus("The user didn't provide an email.  Pressure them further", role='system' )

            user_input = input(f"{self.user_name}: ")
            print("")

            did_provide_email = self.ask_helpful_dumber_gpt( content = f'Does the following string contain an email address?  Please Respond "yes" or "no" only. {user_input}').lower()


        self.user_email = self.ask_helpful_dumber_gpt( content = f'Please return only the email out of the input from the following input: {user_input}')

        self.tell_krampus('Have a small dialogue with the user for a few messages.  Do not assign christmas tasks until prompted.', role = 'system')

        n_exchanges_until_bored = randrange(4) + 2 

        while True:
            
            if(n_exchanges_until_bored <= 0):
                self.tell_krampus(f"""You are now bored. Assign the user three tasks. One from this a predefined list:
                {self.tasks} 
                and two more whimsical tasks of your choosing creates.
                These tasks are meant to entertain Krampus 3000, reflecting its self-interested nature.  Assign the user three tasks in a well-formatted list""")

            # Get user input
            user_input = input(f"{self.user_name}: ")
            print('')

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

            self.type_like_human(f"Krampus_3000: {response.choices[0]['message']['content']} \n")

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

        typing_sound_path = os.path.join(os.path.dirname(__file__), 'assets', 'sounds', 'single_key_press.mp3')

        self.keep_playing_sound = True
        key_press_sounds = multiprocessing.Process(name='p1', 
                                     target=self.play_continuous_staggered_sounds,
                                     args=(typing_sound_path, .05) )
        
        key_press_sounds.start()

        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print('')  # Print a newline at the end

        key_press_sounds.terminate()

    def play_sound_once(self, sound_file):
        """
        Plays a sound file once.

        :param sound_file: Path to the sound file.
        """
        playsound(sound_file)

    def play_continuous_staggered_sounds(self, sound_file, interval=0.2):
        """
        Continuously starts playing a sound file at staggered intervals.

        :param sound_file: Path to the sound file.
        :param interval: Interval in seconds between the start of each sound.
        """

        while True:
            threading.Thread(target=lambda: playsound(sound_file, False), daemon=True).start()
            time.sleep(interval)
