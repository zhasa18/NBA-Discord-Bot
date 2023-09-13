import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "!compare":


        return "Hello there!"
    
    if p_message == "!roll":
        return str(random.randint(1, 6))
    
    if p_message == "!help":
        return "Commands: !help, roll, hello"
    
    return 