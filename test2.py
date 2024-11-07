from shiny import App, ui, reactive, render
import pandas as pd
import joblib

# Load the pre-trained model
model = joblib.load("linear_regression_model.pkl")

# Define available choices for inputs
cities = ["Cupertino", "San Jose", ...]  # Include your full list
home_types = ["SINGLE_FAMILY", "APARTMENT", ...]

# Define the Shiny UI
app_ui = ui.page_fluid(
    ui.h2("House Price Prediction App"),
    ui.input_select("city", "City:", choices=cities),
    ui.input_select("home_type", "Home Type:", choices=home_types),
    ui.input_numeric("bathrooms", "Number of Bathrooms:", value=2),
    ui.input_numeric("bedrooms", "Number of Bedrooms:", value=3),
    # Add more inputs as needed...
    ui.input_action_button("predict", "Predict Price"),
    ui.output_text_verbatim("prediction_output")
)

def server(input, output, session):
    @reactive.event(input.predict)
    def prediction_output():
        input_data = pd.DataFrame({
            f"address/city_{input.city()}": [1],
            f"homeType_{input.home_type()}": [1],
            # Add all other features as needed
        }).reindex(columns=model.feature_names_in_, fill_value=0)

        prediction = model.predict(input_data)[0]
        return f"Predicted House Price: ${prediction:,.2f}"

    output.prediction_output = render.text(prediction_output)

# Run the Shiny app
app = App(app_ui, server)
