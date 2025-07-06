from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

# --- Mapping helper ---
def map_chatbot_to_api_values(org_type, team_size, client_volume=None):
    org_type_mapping = {
        "Insurance Provider / EAS": "Insurance Provider/EAS",
        "Mental Health Practitioner – Private Practice": "Private Practice",
        "Mental Health or Healthcare Provider – Public System": "Public Health Provider",
        "Home Care or Specialized Residential Services": "Home Care/Group Home",
        "Other": "Home Care/Group Home",
    }
    team_size_mapping = {
        "1 (Solo practice)": "1",
        "2–5 providers": "2–5",
        "6–15 providers": "6–15",
        "16–50 providers": "16–50",
        "51+ providers": "51+",
        "Not sure yet": "6–15",
    }
    client_volume_mapping = {
        "Less than 100": "Low",
        "100–500": "Medium",
        "501–1,000": "High",
        "Over 1,000": "Very High",
    }
    mapped_org_type = org_type_mapping.get(org_type.strip(), org_type.strip()) if org_type else ""
    mapped_team_size = team_size_mapping.get(team_size.strip(), team_size.strip()) if team_size else ""
    mapped_client_volume = client_volume_mapping.get(client_volume.strip(), client_volume.strip()) if client_volume else ""

    return mapped_org_type, mapped_team_size, mapped_client_volume

# --- New Smarter Package Prediction ---
def predict_package(org_type, team_size, client_volume=None, specialization=None, service_model=None):
    mapped_org_type, mapped_team_size, mapped_client_volume = map_chatbot_to_api_values(org_type, team_size, client_volume)
    print(f"Mapped values → Org: {mapped_org_type}, Team: {mapped_team_size}, Volume: {mapped_client_volume}")

    if not mapped_org_type or not mapped_team_size:
        raise ValueError("Invalid mapping: org_type or team_size not recognized.")

    if specialization and "trauma" in specialization.lower():
        print("Branch: Specialization Trauma → Practice Plus")
        return 'Practice Plus', 8

    if mapped_client_volume == "Very High":
        print("Branch: Volume Very High → Enterprise Care (Public Health)")
        return 'Enterprise Care (Public Health)', 20

    if service_model and "group" in service_model.lower() and mapped_team_size in ['16–50', '51+']:
        print("Branch: Group model → Community Access")
        return 'Community Access', 20

    if mapped_org_type == "Private Practice":
        if mapped_team_size in ['1', '2–5']:
            return 'Fresh Start', 4
        elif mapped_team_size == '6–15':
            return 'Practice Plus', 8
        elif mapped_team_size == '16–50':
            return 'Community Access', 16
        else:
            return 'Community Access', 20

    elif mapped_org_type == "Public Health Provider":
        if mapped_team_size in ['1', '2–5', '6–15']:
            return 'Practice Plus', 6
        else:
            return 'Enterprise Care (Public Health)', 20

    elif mapped_org_type == "Insurance Provider/EAS":
        return 'Enterprise Access (Insurance & EAS)', 20

    # Fallback
    if mapped_team_size in ['1', '2–5']:
        return 'Fresh Start', 4
    elif mapped_team_size == '6–15':
        return 'Practice Plus', 8
    elif mapped_team_size == '16–50':
        return 'Community Access', 16
    else:
        return 'Community Access', 20

# --- Pricing and Sales Messages ---
PACKAGE_PRICE_TABLE = {
    ('Fresh Start', 4): 196,
    ('Practice Plus', 8): 392,
    ('Practice Plus', 6): 294,
    ('Community Access', 20): 980,
    ('Community Access', 16): 784,
    ('Enterprise Care (Public Health)', 20): 980,
    ('Enterprise Access (Insurance & EAS)', 20): 980,
}

SALES_MESSAGES = {
    "Fresh Start": (
        "Thank you for providing your details. Based on your responses, "
        "we recommend the *Fresh Start* package with {seats} seats.\n\n"
        "**Estimated Price**: ${price}  \n"
        "**Key Features**: {features}  \n"
        "[Click here to find out more]({next_steps})"
    ),

    "Practice Plus": (
        "Thank you for providing your details. Based on your responses, "
        "we recommend the *Practice Plus* package with {seats} seats.\n\n"
        "**Estimated Price**: ${price}  \n"
        "**Key Features**: {features}  \n"
        "[Click here to find out more]({next_steps})"
    ),
    
    "Community Access": (
        "Thank you for providing your details. Based on your responses, "
        "we recommend the *Community Access* package with {seats} seats.\n\n"
        "**Estimated Price**: ${price}  \n"
        "**Key Features**: {features}  \n"
        "[Click here to find out more]({next_steps})"
    ),
    
    "Enterprise Care (Public Health)": (
        "Thank you for providing your details. Based on your responses, "
        "we recommend the *Enterprise Care (Public Health)* package with {seats} seats.\n\n"
        "**Estimated Price**: ${price}  \n"
        "**Key Features**: {features}  \n"
        "[Click here to find out more]({next_steps})"
    ),
    

    "Enterprise Access (Insurance & EAS)": (
        "Thank you for providing your details. Based on your responses, "
        "we recommend the *Enterprise Access (Insurance & EAS)* package with {seats} seats.\n\n"
        "**Estimated Price**: ${price}  \n"
        "**Key Features**: {features}  \n"
        "[Click here to find out more]({next_steps})"
    ),

}

# --- FastAPI App ---
app = FastAPI(
    title="Cogni API",
    description="AI-powered mental health package recommender",
    version="1.0.0"
)

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
    service_model: Optional[str] = None
    specialization: Optional[str] = None
    timeline: Optional[str] = None
    features: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Cogni API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/getRecommendation")
def get_recommendation(data: InputData):
    try:
        print("Received data:", data.dict())

        package, seats = predict_package(
            data.org_type,
            data.team_size,
            data.client_volume,
            data.specialization,
            data.service_model
        )

        next_steps = f"https://cogni-recommendation-chuiv5x8slzxktq3mzbb5p.streamlit.app/?tier={package.replace(' ', '%20')}&seats={seats}"

        key_features = {
            "Fresh Start": "Self-guided tools, AI self-assessment, 1 group session/month, provider dashboard",
            "Practice Plus": "Full AI suite, group modules, custom reports, real-time analytics, provider dashboard",
            "Community Access": "Multilingual AI tools, scalable group support, onboarding support, volume discounts",
            "Enterprise Care (Public Health)": "Unlimited users, robust analytics, API access, client monitoring & support",
            "Enterprise Access (Insurance & EAS)": "API integration, branded self-assessments, usage analytics, outcome dashboards"
        }.get(package, "Comprehensive support and analytics")

        price = PACKAGE_PRICE_TABLE.get((package, seats), seats * 49)
        sales_message = SALES_MESSAGES.get(package, "").format(
    seats=seats,
    price=price,
    features=key_features,
    next_steps=next_steps
)


        return {
            "recommended_package": package,
            "recommended_seats": seats,
            "estimated_pricing": f"${price}",
            "key_features": key_features,
            "next_steps": next_steps,
            "sales_message": sales_message
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("cogni_api:app", host="0.0.0.0", port=10000, reload=True)
