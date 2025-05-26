import os
from dotenv import load_dotenv
from typing_extensions import TypedDict, List, Dict, Any, Optional
from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from memory import log_email

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini')

class EmailState(TypedDict):
    email: Dict[str, Any]
    email_category: Optional[str]
    spam_reason: Optional[str]
    is_spam: Optional[bool]
    email_draft: Optional[str]
    messages: List[Dict[str, Any]]

def read_email(state: EmailState):
    email = state["email"]
    print(f"Reading email from {email['sender']}: {email['subject']}")
    return {}


def classify_email(state: EmailState):
    """Mailer Agent uses an LLM to determine if the email is spam or legitimate"""
    email = state['email']

    # Prompt the LLM
    prompt = f"""
    You are an expert email classifier.

    Classify the following email as either "Spam" or "Legitimate".
    If it's spam, explain why in 1-2 sentences.
    If it's legitimate, also categorize it as one of: inquiry, complaint, thank you, request, information.

    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}

    Respond strictly in this JSON format:
    {{
        "classification": "Spam" or "Legitimate",
        "spam_reason": "...",  # if spam
        "category": "..."      # if legitimate
    }}
    """

    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)

    import json
    import re

    # Extract JSON from the response
    match = re.search(r'\{.*\}', response.content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            is_spam = data.get("classification", "").lower() == "spam"
            spam_reason = data.get("spam_reason") if is_spam else None
            email_category = data.get("category") if not is_spam else None
        except json.JSONDecodeError:
            is_spam = True
            spam_reason = "Could not parse LLM response."
            email_category = None
    else:
        is_spam = True
        spam_reason = "No valid response from LLM."
        email_category = None

    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content}
    ]

    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": new_messages
    }


def handle_spam(state: EmailState):
    print(f"SPAM detected. Reason: {state['spam_reason']}")
    log_email(state, label="spam")
    return {}

def draft_response(state: EmailState):
    email = state["email"]
    category = state.get("email_category", "general")
    prompt = f"""
    Draft a professional response for a {category} email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}
    """
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content}
    ]
    return {
        "email_draft": response.content,
        "messages": new_messages
    }

def notify_user(state: EmailState):
    log_email(state, label="legitimate")
    return {}

def route_email(state: EmailState):
    return "spam" if state["is_spam"] else "legitimate"

# Build Graph
def build_email_graph():
    graph = StateGraph(EmailState)
    graph.add_node("read_email", read_email)
    graph.add_node("classify_email", classify_email)
    graph.add_node("handle_spam", handle_spam)
    graph.add_node("draft_response", draft_response)
    graph.add_node("notify_user", notify_user)

    graph.add_edge(START, "read_email")
    graph.add_edge("read_email", "classify_email")
    graph.add_conditional_edges("classify_email", route_email, {
        "spam": "handle_spam",
        "legitimate": "draft_response"
    })
    graph.add_edge("draft_response", "notify_user")
    graph.add_edge("handle_spam", END)
    graph.add_edge("notify_user", END)
    return graph.compile()
