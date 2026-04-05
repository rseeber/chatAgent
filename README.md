# Chat Agent

This is a demo project written in Python meant to be an asynchronous, autonomous AI Agent. The Agent will be capable of responding to prompts (just like a chatbot), as well as create Events for when it should wake up in the future in order to perform tasks.

The Agent should be setup to never go to sleep indefinitely (it will always have a future event setup).

The agent will be capable of calling various 3rd-party APIs (mediated through a programmed proxy, which performs validation, and enforces read-only behavior).

## Future Ambitions

I would really like to eventually setup functionality where it can text you through some interface on your phone (such as through an Instant Messaging service where it has its own account).