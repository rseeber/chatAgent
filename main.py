import threading
import time

# This is the black box that will eventually hold LLM I/O, 
# as well as calling APIs and creating events.
def chat(prompt):
    print(f"handling chat() on your input: {prompt}")
    return "output"


class Event:
    def __init__(self, prompt, condition):
        self.prompt = prompt
        self.condition = condition

        self.satisfied = False

        threading.Thread(target=self.handleEvent, args=(condition,)).start()

    # threaded function
    def handleEvent(self, condition):
        if condition.type == "timer":
            self.wait(condition.value)
        
        elif condition.type == "expression":
            self.testCondition(condition.value, condition.refresh)

    # threaded function
    def wait(self, t):
        time.sleep(t)
        self.trigger()

    # threaded function
    def testCondition(self, expression, refresh):
        while True:
            if eval(expression):
                self.trigger()
                return
            time.sleep(refresh)

    # call this function when the event is finished
    def trigger(self):
        chat(self.prompt)

# a property of the Event class. Used to determine when the Event should be triggered
class Condition:
    def __init__(self, type, value, refresh=30):
        self.type = type
        self.value = value
        self.refresh = refresh

# threaded function
# the thread that handles user prompts (as opposed to Events created by the agent)
def promptThread():
    while True:
        #TODO: change the window where this does I/O
        prompt = input("> ")
        chat(prompt)


if __name__ == "__main__":
    x = 1
    # create some events
    # triggers after 7 seconds
    e1 = Event("prompt1", Condition(type="timer", value=7, refresh=5))
    # triggers when x == 2 (checked every 5 seconds)
    e2 = Event("prompt2", Condition(type="expression", value="x == 2", refresh=5))
    print("[MAIN]: events created...")
    time.sleep(5)
    print("[MAIN]: assigning x=2....")
    # assign x to 2, which should trigger e2 in the next 5 seconds
    x = 2
    print("[MAIN]: assigned!")
    time.sleep(10)

    # Spawn the chat window. I've waited until after the initial events are 
    # done to make things easier.
    threading.Thread(target=promptThread).start()


"""
#TODO:
    # create an Events object, give it an `args` and `satisfied` property.
    # create a Prompt object, give it an `available` and `data` property.
    # set methods for how to update these objects from external modules.
events = [1, 2, 3, 4, 5]
prompt = ""

# MAIN LOOP
while True:
    # Check for satisfied events
    for e in events:
        if e.satisfied:
            threading.Thread(target=chat, args=e.args).start()
        #   To prevent this loop from consuming too much power, when timing isn't 
        # actually that crucial.
        #   Possibly set to a lower number if |events| becomes too large
        time.sleep(0.1)

    # If there's a new user prompt, handle it
    if prompt.available:
        prompt.available = False
        threading.Thread(target=chat, args=(prompt.data,)).start()
    time.sleep(0.1)
"""
