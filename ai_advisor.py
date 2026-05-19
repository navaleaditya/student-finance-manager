from groq import Groq

client = Groq()  # Automatically reads GROQ_API_KEY from environment

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
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI advisor is currently unavailable. Please check your Groq API key. Error: {str(e)}"


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

    # Build messages list for Groq
    messages = [{"role": "system", "content": system_context}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI advisor unavailable. Please check your Groq API key. Error: {str(e)}"