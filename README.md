# Neutral

Neutral is a project focused on detecting and reducing biases, both conscious and unconscious, in hiring practices. It aims to provide HR departments with tools and insights to help identify and address potential biases in their hiring processes.

The project utilizes a combination of advanced machine learning models, including Gemini, LLaMA, and logistic regression, to analyze hiring data and uncover biases. The findings are then presented through a user-friendly Streamlit-based application, making it accessible for HR professionals to understand and act upon.

## Directory Structure

The project has the following directory structure:

```
.
├── app
│   ├── app.py
│   ├── test.py
│   └── utility.py
├── model
│   ├── _pycache_
│   ├── datasets
│   │   └── genai.py
│   ├── hiring_model_pipeline.pkl
│   ├── logistic_regression.ipynb
│   └── _pycache_
├── static
├── templates
└── upload
```

## Installation

To run the Neutral project, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Create a new virtual environment and activate it.
3. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Neutral application, execute the following command from the project root directory:

```
cd app
streamlit run app.py
```

This will start the application.

## Usage

The Neutral application provides the following functionality:

1. **Bias Detection**: The application analyzes hiring data and identifies potential biases in the hiring process, including both conscious and unconscious biases.
2. **Reporting**: The application generates detailed reports and visualizations to help HR departments understand and address the identified biases.
3. **Recommendations**: The application provides specific recommendations and strategies for improving the fairness and inclusiveness of the hiring process.

To use the application, navigate to `http://localhost:8501` in your web browser and follow the on-screen instructions.

## License

This project is licensed under the [MIT License](LICENSE).
