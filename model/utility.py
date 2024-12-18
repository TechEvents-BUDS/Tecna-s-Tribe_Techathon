# edit later
SYSTEM_PROMPT = """Your name is Neutral. You are a tool that assists in making good hiring decisions."""


# machine learning functions
# ML FILES

# Import joblib to load the saved model
import joblib

def predict_hiring(input_data):

    # Load the pipeline
    pipeline = joblib.load('hiring_model_pipeline.pkl')
    print("Pipeline loaded successfully!")
    """
    Predicts whether a candidate should be hired based on input data.

    Args:
        input_data (dict): A dictionary with keys matching the feature names in the dataset.

    Returns:
        dict: A dictionary containing the prediction (0 or 1) and the probability.
    """
    import pandas as pd

    # Convert input dictionary to a DataFrame
    input_df = pd.DataFrame([input_data])  # Convert single row into a DataFrame

    # Make prediction using the pipeline
    prediction = pipeline.predict(input_df)[0]  # 0 or 1 (Not hired / Hired)
    probability = pipeline.predict_proba(input_df)[0, 1]  # Probability of being hired

    return {
        "prediction": prediction,
        "probability": probability
    }