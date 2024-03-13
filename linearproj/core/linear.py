import requests
import json
from typing import List, Dict

from linearproj.config import CONFIG

label_identifier_map = {
    "bug": CONFIG.linear_bug_label_id,
    "feature-request": CONFIG.linear_feature_request_label_id,
    "neither": CONFIG.linear_engineering_label_id,
}


def update_task_urgency(task_id: str) -> None:
    """
    Updates the urgency of a task in the Linear app.

    Args:
        task_id (str): The ID of the task to update.

    Returns:
        None

    Raises:
        Exception: If the request to update the task fails.
    """
    # Define the GraphQL mutation for updating the urgency of a task
    mutation = r"""
    mutation IssueUpdate {{
        issueUpdate(
            id: "{task_id}",
            input: {{
                priority: {urgency}
            }}
        ) {{
            success
        }}
    }}
    """.format(task_id=task_id, urgency=2)

    # Make a POST request to the GraphQL API
    body = {"query": mutation}
    response = requests.post(
        "https://api.linear.app/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": CONFIG.linear_api_key,
        },
        data=json.dumps(body)
    )

    # Check if the request was successful
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Updated task urgency to HIGH: {task_id}")
    else:
        # Request failed, raise an exception with the error details
        try:
            # Attempt to return a detailed error message from the response body
            error_details = response.json()
        except ValueError:
            # JSON parsing failed, use the status code and text as fallback
            error_details = {
                "status_code": response.status_code,
                "error_message": response.text
            }
        
        raise Exception(f"Failed to update issues: {error_details}")


def get_existing_issues() -> List[Dict[str, str]]:
    """
    Retrieves the existing issues from the Linear app.

    Returns:
        list: A list of dictionaries representing the existing issues with the following
    """
    # Define the GraphQL query for retrieving issues
    query = r"""
    query Team {{
    team(id: "{team_id}") {{
        id
        name

        issues {{
        nodes {{
            id
            identifier
            title
            description
        }}
        }}
    }}
    }}
    """.format(team_id=CONFIG.linear_team_id)

    # Make a POST request to the GraphQL API
    body = {"query": query}
    response = requests.post(
        "https://api.linear.app/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": CONFIG.linear_api_key,
        },
        data=json.dumps(body)
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the existing issues from the response
        existing_issues = response.json()["data"]["team"]["issues"]["nodes"]
        return [
            {
                "id": issue["id"],
                "identifier": issue["identifier"],
                "title": issue["title"],
                "description": issue.get("description", "")
            }
            for issue in existing_issues
        ]
    else:
        # Request failed, raise an exception with the error details
        try:
            # Attempt to return a detailed error message from the response body
            error_details = response.json()
        except ValueError:
            # JSON parsing failed, use the status code and text as fallback
            error_details = {
                "status_code": response.status_code,
                "error_message": response.text
            }
        
        raise Exception(f"Failed to retrieve issues: {error_details}")


def create_linear_task(
        task_name: str, 
        task_description: str, 
        task_classification: str,
    ) -> dict:
    """
    Creates a task in the Linear app using the provided task name, description, and classification.

    Args:
        task_name (str): The name of the task.
        task_description (str): The description of the task.
        task_classification (str): The classification of the task. Must be one of "bug", "feature-request", or "neither".

    Returns:
        dict: The created issue with the following keys:
            - id (str): The ID of the created issue.
            - title (str): The title of the created issue.
            - description (str): The description of the created issue.

    Raises:
        Exception: If the request to create the issue fails.
    """
    identifier = label_identifier_map[task_classification]
    # Define the GraphQL mutation for creating an issue
    mutation = r"""
    mutation IssueCreate {{
    issueCreate(
        input: {{
        title: "{title}"
        description: "{description}"
        teamId: "{team_id}"
        labelIds: ["{label_id}"]
        }}
    ) {{
        success
        issue {{
        id
        title
        description
        }}
    }}
    }}
    """.format(title=task_name, description=task_description, team_id=CONFIG.linear_team_id, label_id=identifier)

    # Make a POST request to the GraphQL API
    body = {"query": mutation}
    response = requests.post(
        "https://api.linear.app/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": CONFIG.linear_api_key,
        },
        data=json.dumps(body)
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the created issue from the response
        created_issue = response.json()["data"]["issueCreate"]["issue"]
        return {
            "id": created_issue["id"],
            "title": created_issue["title"],
            "description": created_issue.get("description", "")
        }
    else:
        # Request failed, raise an exception with the error details
        try:
            # Attempt to return a detailed error message from the response body
            error_details = response.json()
        except ValueError:
            # JSON parsing failed, use the status code and text as fallback
            error_details = {
                "status_code": response.status_code,
                "error_message": response.text
            }
        
        raise Exception(f"Failed to create issue: {error_details}")