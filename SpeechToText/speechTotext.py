import speech_recognition as sr
import os
import threading
from  mtranslate  import translate
from colorama import Fore, Style, init

init(autoreset=True) 

def print_loop():
    while True:
        print(Fore.GREEN + "I am listening..", end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)
        
def Translate_Bengali_to_English(text):
    english_text = translate(text, 'en-us')
    return english_text

def Speech_to_Text():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 34000
    r.dynamic_energy_adjustment_damping=0.01080
    r.dynamic_energy_ratio=1.0
    r.pause_threshold = 0.3
    r.operation_timeout = None
    r.pause_threshold = 0.2
    r.non_speaking_duration = 0.2
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
           print(Fore.GREEN + "I am listening..", end="", flush=True)
           try:
               audio = r.listen(source, timeout=None)
               print("\r" + Fore.LIGHTBLUE_EX + "\nProcessing your speech...", end="", flush=True)
               recognizer_text = r.recognize_google(audio).lower()
               if recognizer_text:
                   translated_text = Translate_Bengali_to_English(recognizer_text)
                   print(Fore.YELLOW + f"\nTranslated Text: "+ translated_text)
                   return translated_text
               else:
                   return ""
           except sr.UnknownValueError:
               recognizer_text = ""
           finally:
               print("\r", end="", flush=True)
           
           os.system('cls' if os.name == 'nt' else 'clear')        
        
        
        stt_thread = threading.Thread(target=Speech_to_Text_Python)
        print_thread = threading.Thread(target=print_loop)
        stt_thread.start()
        print_thread.start()
        stt_thread.join()
        print_thread.join()
        
Speech_to_Text()        