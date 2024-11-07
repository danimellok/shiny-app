from shiny import App, ui, reactive, render
import pandas as pd
import joblib
from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return "Hello, World! Your Flask app is running."

# Run the app on port 3838, accessible from any IP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3838)


# Load the pre-trained model
model = joblib.load("linear_regression_model.pkl")

# Define available choices for inputs
cities = [
    "Cupertino", "San Jose", "Foster City", "Redwood City", "Danville", "La Canada Flintridge", "Soquel", 
    "Santa Clara", "Solana Beach", "Hermosa Beach", "Encino", "Fremont", "Orinda", "La Jolla", "Venice", 
    "South San Francisco", "Los Alamitos", "San Bruno", "West Hollywood", "Newport Beach", "San Mateo", 
    "Santa Barbara", "San Gabriel", "Cypress", "Colma", "Calabasas", "Encinitas", "Redondo Beach", "Glendale", 
    "Rancho Palos Verdes", "Yorba Linda", "Morgan Hill", "Capitola", "Orange", "San Francisco", 
    "Pacific Grove", "Laguna Niguel", "Los Angeles", "Carpinteria", "Torrance", "Woodland Hills", 
    "Poway", "Aptos", "Carlsbad", "Monterey Park", "Goleta", "Fullerton", "Bonny Doon", "Garden Grove", 
    "Hayward", "Diamond Bar", "Placentia", "Santa Cruz", "Brea", "Gilroy", "San Diego", "Anaheim", 
    "Lakewood", "Seaside", "Canoga Park", "West Hills", "Daly City", "Van Nuys", "Santa Clarita", 
    "Los angeles", "Monterey", "Covina", "Newhall", "Salinas", "Valencia", "Norco", "Del Rey Oaks", 
    "Saugus", "Santa Paula", "Long Beach", "Ontario", "Castaic", "Granite Bay", "Ventura", "Seal Beach", 
    "Signal Hill", "BAKERSFIELD", "Bear Valley", "Riverside", "Fontana", "Val Verde", "Roseville", 
    "Oxnard", "Shafter", "Tehachapi", "Marina", "Bakersfield", "Clovis", "Sanger", "Fresno", 
    "Santa Paula", "North Fontana", "Coarsegold"
]

home_types = ["SINGLE_FAMILY", "APARTMENT", "MULTI_FAMILY", "TOWNHOUSE", "CONDO", "MANUFACTURED"]

app_ui = ui.page_fluid(
    ui.h2("House Price Prediction App"),

    # User inputs for each feature
    ui.input_select("city", "City:", choices=cities),
    ui.input_select("home_type", "Home Type:", choices=home_types),
    ui.input_numeric("bathrooms", "Number of Bathrooms:", value=2),
    ui.input_numeric("bedrooms", "Number of Bedrooms:", value=3),
    ui.input_numeric("living_area", "Living Area (sq ft):", value=1500),
    ui.input_numeric("lot_size", "Lot Size (sq ft):", value=5000),
    ui.input_numeric("year_built", "Year Built:", value=2000),
    ui.input_numeric("walkability_score", "Walkability Score:", value=50),

    # Additional inputs for each missing variable
    ui.input_checkbox("resoFacts_fireplaces", "Fireplaces", False),
    ui.input_checkbox("resoFacts_furnished", "Furnished?", False),
    ui.input_checkbox("resoFacts_hasCooling", "Has Cooling?", False),
    ui.input_checkbox("resoFacts_hasHeating", "Has Heating?", False),
    ui.input_checkbox("resoFacts_hasView", "Has View?", False),
    ui.input_checkbox("resoFacts_isNewConstruction", "Is New Construction?", False),
    ui.input_numeric("resoFacts_levels", "Number of Levels:", value=1),
    ui.input_numeric("resoFacts_parkingCapacity", "Parking Capacity:", value=1),
    ui.input_checkbox("coveredParkingBinary", "Covered Parking", False),
    ui.input_checkbox("coastCity", "Coastal City", False),
    ui.input_checkbox("Park_3miles", "Nearby Park (3 miles)?", False),
    ui.input_checkbox("has_HOA", "Has HOA?", False),

    # Single select for restaurant category
    ui.input_select(
        "restaurants_nearby_category",
        "Nearby Restaurant Category:",
        choices=["High", "Medium", "Low"]
    ),

    ui.input_action_button("predict", "Predict Price"),
    ui.output_text_verbatim("prediction_output")  # Registering output correctly
)

def server(input, output, session):
    @reactive.event(input.predict)
    def prediction_output():
        # Prepare input for model, including all variables
        input_data = pd.DataFrame({
            f"address/city_{input.city()}": [1],
            f"homeType_{input.home_type()}": [1],
            "bathrooms": [input.bathrooms()],
            "bedrooms": [input.bedrooms()],
            "livingArea": [input.living_area()],
            "lotSize": [input.lot_size()],
            "yearBuilt": [input.year_built()],
            "walkability_score": [input.walkability_score()],
            "resoFacts/fireplaces": [1 if input.resoFacts_fireplaces() else 0],
            "resoFacts/furnished": [1 if input.resoFacts_furnished() else 0],
            "resoFacts/hasCooling": [1 if input.resoFacts_hasCooling() else 0],
            "resoFacts/hasHeating": [1 if input.resoFacts_hasHeating() else 0],
            "resoFacts/hasView": [1 if input.resoFacts_hasView() else 0],
            "resoFacts/isNewConstruction": [1 if input.resoFacts_isNewConstruction() else 0],
            "resoFacts/levels": [input.resoFacts_levels()],
            "resoFacts/parkingCapacity": [input.resoFacts_parkingCapacity()],
            "coveredParkingBinary": [1 if input.coveredParkingBinary() else 0],
            "coastCity": [1 if input.coastCity() else 0],
            "Park_3miles": [1 if input.Park_3miles() else 0],
            "has_HOA": [1 if input.has_HOA() else 0],
            "restaurants_nearby_category_High": [1 if input.restaurants_nearby_category() == "High" else 0],
            "restaurants_nearby_category_Low": [1 if input.restaurants_nearby_category() == "Low" else 0],
            "restaurants_nearby_category_Medium": [1 if input.restaurants_nearby_category() == "Medium" else 0]
        }).reindex(columns=model.feature_names_in_, fill_value=0)

        # Make the price prediction
        prediction = model.predict(input_data)[0]
        return f"Predicted House Price: ${prediction:,.2f}"

    # Assign the render.text function to the output, triggered by the Predict button
    output.prediction_output = render.text(prediction_output)

app = App(app_ui, server)
