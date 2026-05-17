from langchain_ollama import OllamaLLM 

llm = OllamaLLM(
    model="mistral:7b",
    timeout=120
)

def get_financial_advice(income, spent, status, category_breakdown=None):
    category_text = ""
    if category_breakdown:
        lines = [f"  - {cat}: ₹{amt:.2f}" for cat, amt in category_breakdown.items()]
        category_text = "Spending by category:\n" + "\n".join(lines)

    prompt = f"""
You are a friendly and practical financial advisor for college students in India.

Monthly income: ₹{income}
Total spending this month: ₹{spent}
Status: {status}
{category_text}

Based on the above, give exactly 3 short, practical, and specific tips to help this student manage their finances better.
Focus on their highest spending categories if available.
Keep each tip to 2-3 sentences. Be encouraging, not preachy.
"""
    try:
        return llm.invoke(prompt)
    except Exception as e:
        return f"AI advisor is currently unavailable. Please make sure Ollama is running with Mistral. Error: {str(e)}"

def get_chat_response(income, spent, status, category_breakdown, chat_history, user_message):
    category_text = ""
    if category_breakdown:
        lines = [f"  - {cat}: ₹{amt:.2f}" for cat, amt in category_breakdown.items()]
        category_text = "Spending by category:\n" + "\n".join(lines)

    system_context = f"""You are a friendly financial advisor for college students in India.
The student's financial snapshot:
- Monthly income: ₹{income}
- Total spending this month: ₹{spent}
- Status: {status}
{category_text}
Answer their questions in a helpful, concise, and friendly way."""

    # Build conversation string
    history_text = ""
    for msg in chat_history:
        role = "Student" if msg["role"] == "user" else "Advisor"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = f"{system_context}\n\nConversation so far:\n{history_text}Student: {user_message}\nAdvisor:"

    try:
        return llm.invoke(full_prompt)
    except Exception as e:
        return f"AI advisor unavailable. Make sure Ollama is running. Error: {str(e)}"