from openai import OpenAI
from config import GROQ_API_KEY, GROQ_BASE_URL, CHAT_MODEL
from data_tools import summarize_metrics

def get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")

    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )

def create_action_plan(problem: str):
    client = get_groq_client()
    metrics = summarize_metrics()

    prompt = f'''
You are an AI business operations assistant.

Business problem:
{problem}

Current metrics:
{metrics}

Create a practical action plan with:
1. Problem summary
2. Possible causes
3. Recommended actions
4. Metrics to monitor
5. Governance or risk considerations

Keep the answer clear and concise.
'''

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You create practical, grounded business action plans."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
