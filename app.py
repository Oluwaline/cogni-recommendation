import streamlit as st
from urllib.parse import unquote

# ---- PACKAGE DICTIONARY ----
PACKAGES = {
    'Fresh Start': {
        'ideal_client': 'Solo or small private practice',
        'seats': '2-4 seats',
        'pricing': '$199/month base + $40/seat/month',
        'features': [
            'Basic self-guided tools',
            'AI self-assessment',
            '1 group session/month',
            '1 report template'
        ]
    },
    'Practice Plus': {
        'ideal_client': 'Mental health clinics or private group practices (5-15 providers)',
        'seats': '5-15 seats',
        'pricing': '$299/month base (includes 5 seats) + $35/additional seat',
        'features': [
            'Full AI suite',
            'Group modules',
            '2 sessions/month',
            'Custom reports',
            'Provider dashboard'
        ]
    },
    'Community Access': {
        'ideal_client': 'Group homes, home care services',
        'seats': '10-30 staff, scalable by user volume',
        'pricing': '$299 base (includes 5 seats) + $7.99/user/month with volume discounts',
        'features': [
            'Multilingual AI tools',
            'Group support modules',
            'Onboarding support',
            'Usage dashboard',
            'Volume discounts for 500+ users'
        ]
    },
    'Enterprise Care (Public Health)': {
        'ideal_client': 'Public health institutions, rehabilitation centers, or clinics',
        'seats': '10+ staff, unlimited users',
        'pricing': 'Customized plan starting at $600+/month + fee-for-service contract',
        'features': [
            'Full AI triage',
            'Post-session care',
            'Real-time analytics',
            'API access',
            'Client monitoring & support',
            'Unlimited video, audio, and text-based monitoring tools'
        ]
    },
    'Enterprise Access (Insurance & EAS)': {
        'ideal_client': 'Insurance providers and Employee Assistance Services',
        'seats': 'Unlimited or tiered by number of covered members',
        'pricing': 'Customized plan starting at $600+/month + fee-for-service contract',
        'features': [
            'API integration',
            'Branded self-assessments',
            'Usage analytics',
            'Employer group modules',
            'Outcome dashboards',
            'Unlimited monitoring tools'
        ]
    }
}

# ---- STREAMLIT APP ----

st.set_page_config(page_title="Cogni Package Recommendation", page_icon="🧠", layout="wide")
st.title("🎯 Cogni: Your Personalized Package Recommendation")

# ---- PARSE QUERY PARAMETERS ----
query_params = st.experimental_get_query_params()
recommended_package = None
recommended_seats = None

if "tier" in query_params:
    recommended_package = unquote(query_params["tier"][0])
if "seats" in query_params:
    recommended_seats = unquote(query_params["seats"][0])

if not recommended_package or recommended_package not in PACKAGES:
    st.warning("No recommended package provided! Please use the personalized link from your chatbot.")
    st.stop()

# ---- SHOW RECOMMENDATION ----
st.subheader(f"🎉 Recommended Package: {recommended_package}")
st.write(f"**Recommended Seats:** {recommended_seats if recommended_seats else 'N/A'}")

package = PACKAGES[recommended_package]
st.markdown(f"**Ideal for:** {package['ideal_client']}")
st.markdown(f"**Capacity:** {package['seats']}")
st.markdown(f"**Pricing:** {package['pricing']}")
st.markdown("**Key Features:**")
for feature in package['features']:
    st.write(f"- {feature}")

st.success("This is the package recommended for you based on your needs.")

st.write("---")
st.subheader("🔍 Not sure? Explore All Packages")

# ---- COMPARISON & SWITCH ----
tab_list = list(PACKAGES.keys())
tabs = st.tabs(tab_list)
for tab, pkg_name in zip(tabs, tab_list):
    with tab:
        p = PACKAGES[pkg_name]
        st.markdown(f"**Ideal for:** {p['ideal_client']}")
        st.markdown(f"**Capacity:** {p['seats']}")
        st.markdown(f"**Pricing:** {p['pricing']}")
        st.markdown("**Key Features:**")
        for f in p['features']:
            st.write(f"- {f}")
        if pkg_name == recommended_package:
            st.success("🎯 This is your recommended package.")
        else:
            url = f"?tier={pkg_name.replace(' ', '%20')}&seats={recommended_seats if recommended_seats else ''}"
            if st.button(f"Select {pkg_name}", key=f"select_{pkg_name}"):
                st.experimental_set_query_params(tier=pkg_name, seats=recommended_seats if recommended_seats else '')
                st.rerun()

st.write("---")
st.markdown("**Need more help? Contact our sales team at [support@cogni.ai](mailto:support@cogni.ai) or call (555) 123-4567**")

