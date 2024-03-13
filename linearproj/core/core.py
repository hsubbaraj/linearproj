from linearproj.core.gpt import analyze_conversation_and_generate_function_calls, find_similar_task
from linearproj.core.linear import create_linear_task, get_existing_issues, update_task_urgency

def generate_tasks(conversation):
    """
    Generates tasks in the Linear app based on the given conversation.

    Parameters:
    conversation (list): A list of strings representing the conversation.

    Returns:
    None
    """

    issue_list = get_existing_issues()
    
    function_calls = analyze_conversation_and_generate_function_calls(conversation)

    if len(function_calls) == 0:
        print("No engineering tasks identified in the conversation.")
        return

    for function_call in function_calls:
        similar_task_ids = find_similar_task(function_call, issue_list)
        if len(similar_task_ids) == 0:
        # Create a task in the Linear app using the function call
            created_task = create_linear_task(
                function_call["task_name"],
                function_call["task_description"],
                function_call["task_classification"]
            )
            print(f"Created task: {created_task}")
        else:
            for similar_task_id in similar_task_ids:
                print(f"Found existing task related to issue brought up in conversation: {similar_task_id}")
                update_task_urgency(similar_task_id)