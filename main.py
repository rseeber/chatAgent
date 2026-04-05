import threading
import time

# Project Modules
import gui

class Event:
    def __init__(self, prompt, condition):
        self.prompt = prompt
        self.condition = condition

        self.satisfied = False

        threading.Thread(target=self.__handleEvent, args=(condition,)).start()

    # threaded function
    # This function sets up the process to eventually trigger the Event
    # once the condition is met.
    def __handleEvent(self, condition):
        if condition.type == "timer":
            self.__wait(condition.value)
        
        elif condition.type == "expression":
            self.__testCondition(condition.value, condition.refresh)

    # threaded function
    # Waits for t seconds, then triggers the Event
    def __wait(self, t):
        time.sleep(t)
        self.__trigger()

    # threaded function
    # Tests the expression every `refresh` seconds, triggering 
    # the Event when the expression returns True
    def __testCondition(self, expression, refresh):
        while True:
            if eval(expression):
                self.__trigger()
                return
            time.sleep(refresh)

    # threaded function
    # call this function when the event is finished
    def __trigger(self):
        chat(self.prompt)

# a property of the Event class. Used to determine when the Event should be triggered
class Condition:
    def __init__(self, type, value, refresh=30):
        self.type = type
        self.value = value
        self.refresh = refresh

# called from the gui when the user presses 'send'
def handlePrompt(msg):
    # load the user prompt history
        # TODO
    # load the memories
        # TODO
    # append the new prompt, then generate a response
    return chat(msg)


# threaded function
# the thread that handles user prompts (as opposed to Events created by the agent)
def promptThread():
    while True:
        #TODO: change the window where this does I/O
        prompt = input("> ")
        chat(prompt)

# (Should only be called within a thread!!)
# This is the black box that will eventually hold LLM I/O, 
# as well as calling APIs and creating events.
def chat(prompt):
    print(f"handling chat() on your input: {prompt}")
    return "this is an output", "foo()"


if __name__ == "__main__":

    # Start the GUI as a thread
    #threading.Thread(target=gui.run).start()

    x = 1
    # create some events
    # triggers after 7 seconds
    e1 = Event("prompt1", Condition(type="timer", value=7, refresh=5))
    # triggers when x == 2 (checked every 5 seconds)
    e2 = Event("prompt2", Condition(type="expression", value="x == 2", refresh=5))
    print("[MAIN]: events created...")
    print("[MAIN]: assigning x=2....")
    # assign x to 2, which should trigger e2 in the next 5 seconds
    x = 2
    print("[MAIN]: assigned!")

    # Spawn the chat window. I've waited until after the initial events are 
    # done to make things easier.
    #threading.Thread(target=promptThread).start()

    # Start the GUI in the main thread
    app = gui.ChatUI()
    app.mainloop()