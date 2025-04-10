import streamlit as st
import requests
from datetime import datetime
import pandas as pd
#import pydeck as pdk  # For maps

# Configuration
#st.set_page_config(page_title="TaxiFare Predictor", layout="wide")

# Title and description
st.title('🚖 NYC Taxi Fare Predictor')
st.markdown("""
Predict taxi fares between any two points in New York City using our machine learning API.
""")

# Sidebar with API selection
#with st.sidebar:
#    st.header("API Settings")
#    api_url = st.selectbox(
#        "Select API endpoint",
#        options=[
#            "https://taxifare.lewagon.ai/predict" #LeWagon API
#        ],
#        index=0
#    )
#    st.info("Using: " + api_url)

api_url = 'https://taxifare.lewagon.ai/predict'

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Date & Time")
    pickup_date = st.date_input("Pickup date", datetime.now())
    pickup_time = st.time_input("Pickup time", datetime.now().time())
    passenger_count = st.number_input("👥 Passenger count", 1, 8, 1)

with col2:
    st.subheader("📍 Location Coordinates")
    st.caption("Manhattan coordinates example: -73.98 (long), 40.75 (lat)")
    
    pickup_lon = st.number_input("Pickup Longitude", value=-73.98, format="%.6f")
    pickup_lat = st.number_input("Pickup Latitude", value=40.75, format="%.6f")
    dropoff_lon = st.number_input("Dropoff Longitude", value=-73.99, format="%.6f")
    dropoff_lat = st.number_input("Dropoff Latitude", value=40.76, format="%.6f")

# Interactive Map
#st.subheader("🗺️ Route Visualization")
#map_data = pd.DataFrame({
#    'lat': [pickup_lat, dropoff_lat],
#    'lon': [pickup_lon, dropoff_lon],
#    'color': [[255, 0, 0], [0, 0, 255]]  # Red pickup, blue dropoff
#    })

#st.pydeck_chart(pdk.Deck(
#    map_style='mapbox://styles/mapbox/light-v9',
#    initial_view_state=pdk.ViewState(
#        latitude=pickup_lat,
#        longitude=pickup_lon,
#        zoom=12,
#        pitch=50,
#    ),
#    layers=[
#        pdk.Layer(
#            'ScatterplotLayer',
#            data=map_data,
#            get_position='[lon, lat]',
#            get_color='color',
#            get_radius=100,
#        ),
#        pdk.Layer(
#            'LineLayer',
#            data=pd.DataFrame({'path': [[pickup_lon, pickup_lat], [dropoff_lon, dropoff_lat]]}),
#            get_path='path',
#            get_color=[0, 255, 0],
#            get_width=5,
#        )
#    ],
#))


# Prediction logic
if st.button("💵 Predict Fare", type="primary"):
    pickup_datetime = f"{pickup_date} {pickup_time}"
    
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count
    }

    try:
        with st.spinner('Predicting...'):
            response = requests.get(api_url, params=params, timeout=10)
            
            # DEBUG: Show raw response
            st.write("Status code:", response.status_code)
            st.write("Response text:", response.text)
            
            prediction = response.json().get('fare')
            
            if prediction is not None:
                st.success(f"Predicted Fare: ${prediction:.2f}")
            else:
                st.error("API returned no prediction")
            
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")


# Footer
#st.markdown("---")
#st.caption("""
#Built with Streamlit | API: TaxiFare Model | [Deploy your own API](https://github.com/lewagon/taxifare)
#""")
