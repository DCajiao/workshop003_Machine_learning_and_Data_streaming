# 🌟 Happiness Score Prediction API 🌍

Welcome to the **Happiness Score Prediction API**! This app allows you to predict a country's happiness score using machine learning. It also lets you upload new models and manage the available ones. 🚀

---

## 📂 Folder Structure

Here’s what you’ll find in this repository:

```
api/
├── src/
│   ├── core/
│   │   ├── model_management.py  # Handles model loading and predictions
│   ├── models/
│   │   ├── 00_happiness_score_prediction_model.pkl  # Preloaded model
|   ├── methods.md        # Documentation on endpoints and their use
├── main.py               # Main entry point of the API
├── .dockerignore         # Docker ignored files
├── Dockerfile            # Docker configuration for containerizing the app
├── requirements.txt      # Python dependencies
├── README.md             # Documentation (you're reading it now!)
```

---

## 🚀 Getting Started

You can run this app either using **Python** or **Docker**.

### 🐍 Running with Python

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/happiness-score-api.git
   cd happiness-score-api
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   python main.py
   ```

5. **Access the API**:
   - Open your browser or a tool like Postman and go to: `http://localhost:5000`.

---

### 🐳 Running with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t happiness-score-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 happiness-score-api
   ```

3. **Access the API**:
   - Open your browser or a tool like Postman and go to: `http://localhost:5000`.

---

## 🌟 Features

Here’s what you can do with the API:

### 🔍 1. View Documentation
- **Path**: `/`
- **Method**: `GET`
- **Description**: Get this documentation as HTML.

### 📊 2. Predict Happiness Score
- **Path**: `/predict`
- **Method**: `POST`
- **Description**: Send input features and get a prediction.
- **Example Request**:
   ```json
   {
     "feature1": 1.0,
     "feature2": 2.0
   }
   ```
- **Example Response**:
   ```json
   {
     "prediction": 7.5
   }
   ```

### 📥 3. Upload a New Model
- **Path**: `/upload_model`
- **Method**: `POST`
- **Description**: Upload and load a new model file (`.pkl`).
- **Example Response**:
   ```json
   {
     "message": "New model uploaded and loaded successfully.",
     "model_path": "./models/01_happiness_score_prediction_model.pkl"
   }
   ```

### 📂 4. List Available Models
- **Path**: `/models`
- **Method**: `GET`
- **Description**: See all models available in the `models` folder.
- **Example Response**:
   ```json
   {
     "models": ["00_happiness_score_prediction_model.pkl"]
   }
   ```

## 🚀 Deployed Version
I invite you to take a look at the API deployed in the free Render service at [happiness-score-prediction-api.onrender.com](https://happiness-score-prediction-api.onrender.com)

---

## 🛠️ How to Contribute

Want to make this API even better? Here’s how you can contribute:

1. Fork the repository 🍴
2. Create a new branch for your feature/bugfix:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes 📝:
   ```bash
   git commit -m "Add some amazing feature"
   ```
4. Push to your branch 🚀:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a pull request 🛠️

---

## 🧪 Testing the API

You can test the API endpoints using tools like:
- [Postman](https://www.postman.com/)
- `curl` (CLI)

Example for predicting happiness:
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"feature1": 1.0, "feature2": 2.0}'
```

---

## ⚡ Technologies Used

- **Python** 🐍
- **Flask** 🌐
- **Scikit-learn** 🤖
- **Docker** 🐳 (optional)

---

## 🛡️ License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as you wish!

---

Made with ❤️ by [DCajiao](https://github.com/DCajiao)
```

Feel free to customize the links, your username, or any other details!