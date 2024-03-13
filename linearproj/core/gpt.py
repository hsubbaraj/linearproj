import openai
import json
from typing import List, Dict

from linearproj.config import CONFIG

def analyze_conversation_and_generate_function_calls(conversation: str) -> List[Dict[str, str]]:
    """
    Analyzes a product conversation and generates function calls based on the identified engineering tasks.

    Args:
        conversation (str): The product conversation to be analyzed.

    Returns:
        list: A list of dictionaries representing the function calls generated from the identified tasks. Each dictionary has the following keys:
            - task_name (str): The name of the task.
            - task_description (str): The description of the task.
            - task_classification (str): The classification of the task. Must be one of "bug", "feature-request", or "neither".

    Raises:
        Exception: If the request to GPT fails.
    """
    prompt = f"Given a product conversation, do the following:\n1. Identify all the possible engineering tasks from the product conversation.\n2. For each task, create a dictionary with the following keys:\n    - task_name (str): The name of the task.\n    - task_description (str): The description of the task.\n    - task_classification (str): The classification of the task. Must be one of \"bug\", \"feature-request\", or \"neither\".\n3. Return a JSON object with a key function_calls that contains the list of dictionaries created in step 2.\n\nProduct Conversation:\n{conversation}"
    openai.api_key = CONFIG.openai_api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the latest available model, e.g., gpt-4
        messages=[
            {"role": "system", "content": "You are a highly intelligent AI trained to analyze product conversations and identify engineering tasks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        n=1,
        response_format={"type": "json_object"},
    )

    # Assuming the response format aligns with the expectation of extracting 'function_calls'
    # Extract the function calls from the response
    if response.choices[0]:
        response_json = json.loads(response.choices[0].message.content)
        function_calls = response_json.get('function_calls', [])
        return function_calls
    else:
        raise Exception(f"GPT unexpected output: {response}")
    

def find_similar_task(current_issue, issue_list):
    """
    Finds a similar task in the existing issue list based on the current issue.

    Args:
        current_issue (dict): The current issue to be compared.
        issue_list (list): A list of dictionaries representing the existing issues.

    Returns:
        list: list of similar tasks. Can be empty if no similar tasks are found.
    """

    prompt = f"Given a current engineering issue and a list of existing engineering issues with the below structure \n    \"id\": <issue id>,\n    \"identifier\": <issue identifier>,\n \"title\": <title of issue>,\n    \"description\": <description of issue>\n\ndo the following:\n1. Analyze the existing issues and see if any are at least 80% similar to the provided current issue.\n2. Return a JSON object with the key issue_identifiers that has a list of the identifiers of the identified existing issues.\n3. If there are no existing issues that are at least 80% similar, return a JSON object with the key issue_identifiers that has an empty list.\n\nCurrent Issue:\n{current_issue}\n\nExisting Issues:\n{issue_list}"

    openai.api_key = CONFIG.openai_api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the latest available model, e.g., gpt-4
        messages=[
            {"role": "system", "content": "You are a highly intelligent AI trained to compare new engineering tickets to existing ones."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500,
        n=1,
        response_format={"type": "json_object"},
    )
    
    # Assuming the response format aligns with the expectation of extracting 'function_calls'
    # Extract the function calls from the response
    if response.choices[0]:
        response_json = json.loads(response.choices[0].message.content)
        issue_identifiers = response_json.get('issue_identifiers', [])
        return issue_identifiers
    else:
        raise Exception(f"GPT unexpected output: {response}")
