from linearproj.config import load_config
from linearproj.core.core import generate_tasks

def load_conversation(conversations_path):
    with open(conversations_path, "r") as file:
        conversations = file.read()
    return conversations.strip()

def main():
    config = load_config()

    for conversation_path in config.conversation_paths:
        conversation = load_conversation(conversation_path)
        print(f"Loaded conversation from: {conversation_path}")
        generate_tasks(conversation)
        print(f"Finished generating tasks for conversation from: {conversation_path}")

if __name__ == "__main__":
    main()