import streamlit as st
import openai
import os

st.set_page_config(page_title="GreenPath Nepal", layout="centered")
st.title("🌿 GreenPath Nepal")
st.markdown("**Travel Nepal beautifully, leave it even more beautiful**  \nनेपाल घुमौँ सुन्दर तरिकाले, छोडौँ अझ सुन्दर बनाएर।")

# --- API Key Setup ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.warning("⚠️ Please set your OpenAI API key in the environment variable `OPENAI_API_KEY`")
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if api_key:
        openai.api_key = api_key
else:
    openai.api_key = api_key

# --- User Input ---
col1, col2 = st.columns(2)
destination = col1.selectbox("Where do you want to go?", 
                             ["Kathmandu Valley", "Pokhara", "Chitwan National Park", 
                              "Everest Region", "Lumbini", "Annapurna Circuit", "Mustang"])
days = col2.slider("How many days?", 1, 10, 3)

budget = st.selectbox("Budget level", ["Low (homestay & bus)", "Medium", "High"])
priority = st.multiselect("What do you love most?", 
                          ["Nature & Trekking", "Culture & Temples", "Adventure", "Relaxation", "Wildlife"], 
                          default=["Nature & Trekking"])

if st.button("🌟 Create My Eco Itinerary"):
    if not openai.api_key:
        st.error("❌ Please provide a valid OpenAI API key to generate your itinerary.")
    else:
        with st.spinner("AI is planning your sustainable trip..."):
            
            prompt = f"""
            You are a Nepal sustainable tourism expert. Create a {days}-day eco-friendly itinerary for {destination}.
            Budget: {budget}. Priorities: {', '.join(priority)}.
            Rules:
            - Use bus, shared jeep, or walking instead of flights
            - Recommend local homestays and family-run restaurants
            - Avoid overcrowded spots, suggest off-season or alternative routes
            - Include daily carbon footprint tip
            - Add safety tips (monsoon, altitude, etc.)
            - Write in simple English with short Nepali translation for each day
            - Format: Day 1: Title – Activities – Stay – Eco Tip
            """
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                
                itinerary = response.choices[0].message.content
                
                st.success("Your GreenPath Nepal Itinerary is Ready!")
                st.markdown(itinerary)
                
                # Carbon footprint estimate (simple)
                footprint = days * 15 if "bus" in itinerary.lower() else days * 40
                st.info(f"🌍 Estimated carbon footprint: {footprint} kg CO₂\nOffset it here: ripple-nepal.org")
                
                # PDF Download
                st.download_button("📄 Download as PDF", itinerary, file_name=f"GreenPath_Nepal_{destination}.txt")
                
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error generating itinerary: {str(e)}")