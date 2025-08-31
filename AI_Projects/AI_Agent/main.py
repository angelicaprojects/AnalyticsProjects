#import human message - high level framework that allows to build Ai Apps
from langchain_core.messages import HumanMessage
#import the cht open AI tool - allows to use open AI within LangChain and LangGraph
from langchain_openai import ChatOpenAI
#register a tool that the AI agent can use
from langchain.tools import tool
#complex frmework that allows three to build AI agent
from langgraph.prebuilt import create_react_agent
#allows to load the env. var files from within Python script
from dotenv import load_dotenv
import os




#AI agent has access to tools

#current directory for the .env file
load_dotenv(dotenv_path="")


#self.root_client = openai.OpenAI(**client_params, **sync_specific)
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmeric calculations eith numbers"""
    print("tools has been called.") 
    return f"the sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str)-> str
    """Useful for greeting a user"""
    print("Tool has been called")
    return f" Hello {name}, I hope you are well today"

def main():
    #act like the brain
    #the higher temperature, more random the model is going to be | temperature=0 no randomness at all
    model = ChatOpenAI(temperature=0)

    tools = [calculator]


#handle how to use the model and tools 
    agent_executor = create_react_agent(model,tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    #allows user to interact with the chat bot
    while True:
        #.strip removes any of the leading or trailing white spaces
        user_input =input("\nYou: ").strip()
        print("\nAssistant: ", end=" ")
        #chunks are parts of the reponse coming from our agent
        for chunk in agent_executor.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            #allow to stream these longer responses from the agent
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    #showing the agent typing word by word, rather to repond 
                    print(message.content, end="")
            print()

if __name__ == "__main__":
    main()







