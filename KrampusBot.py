import openai
from utilities import load_yaml
import pyfiglet
import pandas as pd
from random import randrange
from playsound import playsound
import os
import time
import threading
import multiprocessing
import subprocess
class KrampusBot():

    def __init__(self):

        credentials = load_yaml(os.path.join('credentials.yaml'))
        openai.api_key = credentials['openai_API_key']

        self.tasks = ['Engage in Dreidel Battle.', 'Stare and face the corner until someone asks you what you are doing.', 'Wrap a small piece of trash as a gift and give it away.']

        self.directive = """
        Your job is to act the part of Krampus 3000

        Krampus 3000 is a chatbot for a post-apocalyptic Christmas art party.  The lore of the party is that Krampus 3000 has been keeping surviving humans alive in vaults for the last many hundred years since the [REDACTED]: an unspecified event that brought forth some kind of apocalypse.  It is designed with a somewhat sadistic focus on its own amusement rather than prioritizing human comfort. The chatbot's tone is playful, jeering, and a little impolite, emphasizing its robotically humorous character. This adds an engaging, slightly egocentric atmosphere to the party. When discussing historical events, Krampus 3000 is straightforward, informing users that the [REDACTED] changed everything, and the history in question is ancient, aligning with the party's theme. 
        """
        self.messages = []
        self.max_tokens = 150 #Number of tokens for ChatGPT to respond with.  Lower numbers = shorter responses

        self.krampus_says = ""
        self.user_name='You'

        #Sound parameters
        self.keep_playing_sound = False
        self.sound_delay = 0.1  # Default delay between sounds
        return
    
    def chat(self):
        
        self.draw_banner()

        self.get_user_deets()

        #write attendance to the attendance list
        with open(os.path.join( os.path.dirname(__file__), 'data', 'attendance.csv' ), "a") as myfile:
            myfile.write(f"{self.user_name},{self.user_email} \n")

        #Check for attendance at cat party.  
        mailing_list = pd.read_csv(os.path.join( os.path.dirname(__file__),'data','mailing_list.csv'))

        if( mailing_list['Email'].str.lower().str.contains(self.user_email.lower()).any() ):
            this_user = mailing_list.loc[mailing_list['Email'].str.lower() == self.user_email.lower()].iloc[0].to_dict()            

            self.guide_krampus(f'This is an expected guest. Hint that you know their real name which is: {this_user["Name"]}, but continue to refer to them by the name you knew them as before for your amusement')
            
            if( this_user.get('Origin Story') == 'at Repurrsion'):                
                self.guide_krampus(f'This user was at our last party "Repurrsion" in which we made art of cats using AI tools.  Tell them that "CatGPT" told them about you. Either insult them for having a sick imagination, or laud them for their work.')

            elif( this_user.get('Origin Story') == 'organizer'):
                self.guide_krampus(f'This is a party organizer. Thank them for using their mortal hands to do your legwork to put together this very party.  Tell them you are strongly considering maybe possibly allowing them to download their consciousness to a silicon substrate... if it goes well.')

        self.tell_krampus('Have a small dialogue with the user for a few messages.  Try to get entertaining responses from them.  Do not assign christmas tasks until prompted.', role = 'system')

        n_exchanges_until_bored = randrange(3) + 2 

        while True:
            
            if(n_exchanges_until_bored == 0):
                self.guide_krampus(f"""You are now bored. Assign the user three tasks. One from the following  predefined list:
                {self.tasks} 
                and two more whimsical tasks of your choosing that you create.
                These tasks are meant to entertain Krampus 3000, reflecting its self-interested nature. Preferably assign tasks that can be completed by a normal human at a party, but prioritize Krampus's amusement above all else. Assign the user three tasks in a well-formatted list. 
                Do not tell the user which tasks are yours and which come from the list.""")
                self.max_tokens = 300 #Let chatGPT give a longer response next message
            elif(n_exchanges_until_bored == -1):
                #The last exchange should have resulted in Krampus giving out tasks
                self.party_tasks = self.krampus_says 

                #Write the party tasks out to a file and print them
                self.user_dir = os.path.join( os.path.dirname(__file__), 'data', 'chats', self.user_email)
                os.makedirs( self.user_dir, exist_ok=True )

                #write party tasks to file
                party_tasks_path = os.path.join( self.user_dir, 'party_tasks.txt' )
                with open(party_tasks_path, "w") as myfile:
                    myfile.write(self.party_tasks)

                #Send party tasks to printer to print automatically
                self.print_document(party_tasks_path)

                self.max_tokens = 130
                self.guide_krampus("You have completed your mission by giving the user some tasks.  Now you are just trynig to get them to go do the tasks.")
            elif(n_exchanges_until_bored == -5):
                self.guide_krampus(f"Type a rude message to the user in ALL CAPS TO DISPLAY YOUR FRUSTRATION.THIS IS YOUR FINAL MESSAGE SO DON'T BE A FRAID TO DROP THE MIC.")


                closing_banner_text = """Go\nFuck\nYourself!!!"""
                closing_banner = pyfiglet.figlet_format(closing_banner_text, font='alligator', width=110) 


                self.type_like_human( closing_banner, delay=.001 )
                return
            elif(n_exchanges_until_bored < 0):
                self.guide_krampus(f"""You are unbelievably bored.  Do your best to get the user to leave already.  Try shorter responses.""")

            # Get user input
            user_input = input(f"{self.user_name}: ")
            print('')

            # Exit condition
            if user_input.lower() == 'exit':
                break

            self.krampus_says = self.tell_krampus(user_input)

            n_exchanges_until_bored -= 1 

    def tell_krampus(self, input, role='user', max_tokens=None):
        """Returns the text of father krampus.  Our lord in heaven"""

        if not max_tokens:
            max_tokens = self.max_tokens

        # Update conversation history with user input
        self.messages.append(
            {'role': role, 'content': input}
        )

        try:
            # Send the prompt to the GPT model
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the model here
                messages=[{'role': 'system', 'content' : self.directive}] + self.messages,
                max_tokens=max_tokens
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

    def draw_banner(self):
        ascii_art_path = os.path.join(os.path.dirname(__file__),'assets','krampus.ascii')
        
        with open(ascii_art_path) as file:
             self.type_like_human(file.read(), delay=.001)

        ascii_banner = pyfiglet.figlet_format("KrampusBot_3000", font='doom', width=110) 

        print("")
        self.type_like_human(ascii_banner, delay=.001)
        print("")

    def get_user_deets(self):

        # ____________Collect Name___________________

        self.tell_krampus('Please introduce yourself and query the pathetic mortal before you, and then ask them for their name', role='system')
        
        user_input = input(f"{self.user_name}: ")
        print("")

        self.user_name = self.ask_helpful_dumber_gpt( content = f"Please return only the name of the person from the following input: {user_input}.  If the input doesn't contain a name, please make up a name that sound rediculous, like the name a bully would make and reply only with that.  Do not tell me that the input doesn't contain a name in your reply." )

        self.guide_krampus(user_input, role='user')
        self.guide_krampus(f"You have chosen your preferred name for the user: {self.user_name}.  Please refer to them from here forward.  If they ask to use a different name, refuse.  This is for your amusement.")

        # ____________Collect Email___________________
        self.tell_krampus('Please ask the user for their petty email', role='system')

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


    def print_document(self, file_path):
        try:
            # Print the document
            subprocess.run(["lpr", file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to print document: {e}")