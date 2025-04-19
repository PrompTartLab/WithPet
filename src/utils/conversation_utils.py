def get_history(
    question: str,
    messages: list,
) -> dict:
    """
    Generates enhanced input by adding previous conversation history as context to the current question.

    Args:
        question: Current user question
        messages: List of conversation messages stored in session

    Returns:
        dict: Input dictionary containing the enhanced question
    """
    # Only add context if there is sufficient conversation history
    if len(messages) > 2:
        # Build conversation history string
        conversation_history = ""
        # Exclude last user question (already included in question)
        for i in range(len(messages) - 1):
            msg = messages[i]
            role_prefix = "User: " if msg["role"] == "human" else "Assistant: "
            conversation_history += f"{role_prefix}{msg['message']}\n\n"

        # Generate expanded question with conversation context
        enhanced_question = f"""Previous conversation:
{conversation_history}

User's new question: {question}

Please answer the user's new question considering the conversation context above."""

        return {"question": enhanced_question}
    else:
        # Use question as-is for first question
        return {"question": question}
