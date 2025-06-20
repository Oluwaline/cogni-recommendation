from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from any frontend (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    org_type: str
    team_size: str
    client_volume: str

# --- Sales messages for each package ---
SALES_MESSAGES = {
    "Fresh Start": (
        "Thank you for providing your details. Based on your responses, we recommend the *Fresh Start* package with {seats} seats. "
        "This plan offers essential self-guided tools, AI-powered assessments, and a user-friendly dashboard to help you launch your mental health services efficiently and affordably. "
        "[Click here to view your personalized proposal and explore additional options]({next_steps})."
    ),
    "Practice Plus": (
        "Thank you for providing your details. Based on your responses, we recommend the *Practice Plus* package with {seats} seats. "
        "This comprehensive plan delivers full AI-powered assessments, real-time progress dashboards, customizable group therapy modules, and advanced analytics to drive better outcomes. "
        "[Click here to view your personalized proposal and discover exclusive benefits available to your organization]({next_steps})."
    ),
    "Community Access": (
        "Thank you for providing your details. Based on your responses, we recommend the *Community Access* package with {seats} seats. "
        "This package provides scalable group support modules, multilingual AI tools, and special volume pricing to empower large teams and community organizations. "
        "[Click here to view your personalized proposal and learn more]({next_steps})."
    ),
    "Enterprise Care (Public Health)": (
        "Thank you for providing your details. Based on your responses, we recommend the *Enterprise Care (Public Health)* package with {seats} seats. "
        "This solution is tailored for public health organizations, offering unlimited user support, robust analytics, and dedicated client monitoring to ensure the highest standards of care. "
        "[Click here to view your personalized proposal and request a customized consultation]({next_steps})."
    ),
    "Enterprise Access (Insurance & EAS)": (
        "Thank you for providing your details. Based on your responses, we recommend the *Enterprise Access (Insurance & EAS)* package with {seats} seats. "
        "This package offers API integration, branded self-assessments, employer group modules, and unlimited monitoring tools—perfect for insurance providers and EAS programs. "
        "[Click here to view your personalized proposal and discuss your organization’s unique needs]({next_steps})."
    ),
}

# --- Package assignment logic ---
def predict_package(org_type, team_size, client_volume):
    if org_type == "Private Practice":
        if team_size in ['1', '2–5']:
            return 'Fresh Start', 4
        elif team_size == '6–15':
            return 'Practice Plus', 8
        else:
            return 'Community Access', 16
    elif org_type == "Public Health Provider":
        return 'Enterprise Care (Public Health)', 20
    elif org_type == "Insurance Provider/EAS":
        return 'Enterprise Access (Insurance & EAS)', 20
    else:  # Home Care/Group Home
        if team_size in ['1', '2–5', '6–15']:
            return 'Practice Plus', 6
        else:
            return 'Community Access', 20

@app.post("/getRecommendation")
def get_recommendation(data: InputData):
    package, seats = predict_package(
        data.org_type, data.team_size, data.client_volume
    )
    next_steps = f"https://your-streamlit.app/?tier={package.replace(' ', '%20')}&seats={seats}"
    key_features = {
        "Fresh Start": "Self-guided tools, AI self-assessment, 1 group session/month, provider dashboard",
        "Practice Plus": "Full AI suite, group modules, custom reports, real-time analytics, provider dashboard",
        "Community Access": "Multilingual AI tools, scalable group support, onboarding support, volume discounts",
        "Enterprise Care (Public Health)": "Unlimited users, robust analytics, API access, client monitoring & support",
        "Enterprise Access (Insurance & EAS)": "API integration, branded self-assessments, usage analytics, outcome dashboards"
    }.get(package, "Comprehensive support and analytics")

    sales_message = SALES_MESSAGES.get(package, "").format(seats=seats, next_steps=next_steps)

    return {
        "recommended_package": package,
        "recommended_seats": seats,
        "estimated_pricing": f"${seats * 49}",
        "key_features": key_features,
        "next_steps": next_steps,
        "sales_message": sales_message
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("cogni_api:app", host="0.0.0.0", port=10000)
