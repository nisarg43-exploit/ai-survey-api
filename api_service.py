from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
import os

# === Secure API key from environment ===
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# === Survey model ===
class SurveyInput(BaseModel):
    company_name: str
    industry: str
    revenue: str
    employees: str
    What_is_your_biggest_problem__Please_answer_in_detail: str
    goals: List[str]
    tools: List[str]
    company_summary: Optional[str] = "N/A"
    bottlenecks: Optional[str] = "Not specified"
    technology_automation: Optional[str] = "Not specified"

# === Prompt builder ===
def build_prompt(survey_data: SurveyInput):
    goals = ", ".join(survey_data.goals)
    tools = ", ".join(survey_data.tools)

    return f"""
You are an experienced business consultant. A customer has filled out a business survey describing their situation and problems.

Generate two separate outputs based on the data:

---

SECTION 1: INTERNAL CONSULTANT ONLY  
(This is only for internal use by our consulting team.)

• Clearly summarize the customer's top three business problems.  
• Identify any emotional or practical barriers they may be facing (e.g., overwhelm, budget constraints, tool limitations).  
• Provide industry-relevant insights and best practices related to their situation.  
• Recommend actionable solutions that could realistically be delivered in a 1-hour consultation.  
• List 4–5 prioritized next steps we could help them take immediately.

---

SECTION 2: SHORT CUSTOMER TEASER  
(This message is written directly for the customer.)  

• Begin with a warm, empathetic acknowledgment of their unique challenges, showing that we understand their current business situation.  
• Reflect the core of their brand mission or values to demonstrate genuine connection.  
• Give them one practical, high-impact solution or insight they can act on right away to start improving.  
• Reassure them that their bigger business problems can be solved with the right guidance.  
• Reinforce our credibility and commitment to helping them grow.   
• End by affirming that we’re looking forward to the upcoming consulting session, which is already scheduled and paid for.

---

Customer Data:
Company Name: {survey_data.company_name}
Industry: {survey_data.industry}
Revenue: {survey_data.revenue}
Employees: {survey_data.employees}

Biggest Business Problem (Detailed):
{survey_data.What_is_your_biggest_problem__Please_answer_in_detail}

Business Goals: {goals}
Current Tools and Technologies: {tools}

Company Summary:
{survey_data.company_summary}

Workflow Bottlenecks:
{survey_data.bottlenecks}

Technology and Automation:
{survey_data.technology_automation}
    """.strip()

# === OpenAI call ===
def generate_response(prompt: str, model: str = "gpt-4o-mini"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a strategic consultant representing a business services agency."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=850,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === API route ===
@app.post("/generate_diagnosis")
def get_ai_diagnosis(input_data: SurveyInput):
    prompt = build_prompt(input_data)
    result = generate_response(prompt)
    return {"diagnosis": result}