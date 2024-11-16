# Happiness Score Prediction API

This API predicts the Happiness Score of a country using a machine learning model in `.pkl` format. Additionally, it allows uploading new models and managing available ones.

## Endpoints

### 1. **Get Documentation**
- **Path**: `/`
- **Method**: `GET`
- **Description**: Returns this documentation file.
- **Responses**:
  - **200**: Returns the documentation in HTML format.
  - **404**: `README.md` file not found.
  - **500**: Unexpected error while retrieving the documentation.

---

### 2. **Predict Happiness Score**
- **Path**: `/predict`
- **Method**: `POST`
- **Description**: Predicts the Happiness Score based on input features.
- **Request Body** (JSON):
  ```json
  {
    "feature1": value,
    "feature2": value,
    ...
  }
  ```
- **Responses**:
  - **200**: Returns the prediction.
    ```json
    {
      "prediction": <predicted_value>
    }
    ```
  - **400**: Invalid input JSON or no data provided.
    ```json
    {
      "error": "Invalid JSON input."
    }
    ```
  - **500**: Internal error during prediction.
    ```json
    {
      "error": "Error during prediction."
    }
    ```

---

### 3. **Upload a New Model**
- **Path**: `/upload_model`
- **Method**: `POST`
- **Description**: Uploads and loads a new machine learning model.
- **Request**: A file upload containing the model in `.pkl` format.
- **Responses**:
  - **200**: Model uploaded and loaded successfully.
    ```json
    {
      "message": "New model uploaded and loaded successfully.",
      "model_path": "./models/<model_file_name>"
    }
    ```
  - **400**: No file provided in the request.
    ```json
    {
      "error": "No model file provided."
    }
    ```
  - **500**: Internal error during the upload or loading process.
    ```json
    {
      "error": "Error uploading and loading new model."
    }
    ```

---

### 4. **List Available Models**
- **Path**: `/models`
- **Method**: `GET`
- **Description**: Returns a list of available models in the `models` directory.
- **Responses**:
  - **200**: Returns the list of model file paths.
    ```json
    {
      "models": ["model1.pkl", "model2.pkl", ...]
    }
    ```
  - **500**: Internal error while listing models.
    ```json
    {
      "error": "Error showing models."
    }
    ```

---

## How to Run the API

1. Clone this repository.
2. Ensure Python is installed (version 3.7 or higher).
3. Install dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the API:
   ```bash
   python main.py
   ```
5. Access the API at `http://localhost:5000`.

---

## Example Usage

### Predict Happiness Score
1. Make a POST request to `/predict` with the required JSON payload.
2. Example using `curl`:
   ```bash
   curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"feature1": 1.0, "feature2": 2.0}'
   ```

### Upload a New Model
1. Make a POST request to `/upload_model` with a `.pkl` file.
2. Example using `curl`:
   ```bash
   curl -X POST http://localhost:5000/upload_model -F "model=@path_to_model.pkl"
   ```

---

## Error Codes
- **200**: Request successful.
- **400**: Client error (e.g., missing or invalid data).
- **404**: Resource not found.
- **500**: Internal server error.