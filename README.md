# Conversation Analysis -> Linear Tasks

## Description
This project takes in product conversations and generates Linear tasks out of them. Roughly does the following:
1. Asks GPT to analyze a given conversation and see if there are any eng tasks it can create out of it.
2. Asks GPT to compare the potential tasks to the existing tasks of the project
    - If there are no similar exisiting tasks, create a task
    - If there are similar existing tasks, update the urgency of the tasks to HIGH.


## Future Improvements

1. Should run a batch job to pull all the active linear tasks and embed them in a vectorDB.
2. Compare the embedding of the potential task to the active tasks, create if necessary.
3. Write all the activity to some time-series DB vs printing on the console.

## Installation

```
conda create --name llmenv python=3.10
conda activate llmenv
cd linearproj
make install
```

## Usage

First create a file called `config.py` that has all the requisite information from `config-example.py`.
Then run `make run`

### Tests

There are 3 conversations in `tests/conversations`. 1 and 2 are duplicates to show how the updates work. 


```
(llmenv) MacBook-Pro:linearproj Hari$ make run
poetry run python3 server.py
Loaded conversation from: ../tests/conversations/conversation1.txt
Created task: {'id': '6fd31fa0-4c13-40ab-87b6-f0f49ea81bcb', 'title': 'Enhance Natural Language Processing for Complex Queries', 'description': "Enhance the AI assistant's natural language processing capabilities to better understand and respond to complex product queries."}
Created task: {'id': '32f08285-6f30-4dac-bcc6-876eb86d97ff', 'title': 'Improve CRM Integration', 'description': 'Develop a more robust API connection between the CRM system and the AI assistant to streamline data syncing and automation.'}
Finished generating tasks for conversation from: ../tests/conversations/conversation1.txt
Loaded conversation from: ../tests/conversations/conversation2.txt
Found existing task related to issue brought up in conversation: HAR-33
Updated task urgency to HIGH: HAR-33
Found existing task related to issue brought up in conversation: HAR-34
Updated task urgency to HIGH: HAR-34
Finished generating tasks for conversation from: ../tests/conversations/conversation2.txt
Loaded conversation from: ../tests/conversations/conversation3.txt
Created task: {'id': '93d9b8f2-a15d-4608-8ad1-e12b37c071d4', 'title': 'Enhance audio processing for better quality in large meetings', 'description': 'Implement advanced audio filtering algorithms and possibly integrate machine learning models to reduce background noise and echo during large meetings.'}
Created task: {'id': '36e0e437-f4d4-4bf8-8896-c2fc3360047c', 'title': 'Develop a smarter scheduling system for handling time zones', 'description': 'Create a more intuitive time zone management feature that automatically adjusts meeting times for participants in different time zones and integrates with external calendars.'}
Finished generating tasks for conversation from: ../tests/conversations/conversation3.txt
```