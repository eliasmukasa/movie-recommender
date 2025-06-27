# 🎬 Movie Recommendation Engine

A full-stack application featuring a machine learning model deployed as a live web service to provide real-time movie recommendations.

## 🚀 Live Demo

Check out the live, deployed application here: [https://mlproject.eliaskizito.com](https://mlproject.eliaskizito.com)

screenshot.png 

---

## 📖 About The Project

This project demonstrates an end-to-end machine learning workflow, from data processing to deploying a model as a public-facing web service. The core of the application is a Python backend that runs continuously on a cloud server, exposing a REST API built with Flask. This API serves predictions from a content-based filtering model that was trained on the MovieLens dataset using Scikit-learn.

The API is consumed by a lightweight, responsive frontend built with vanilla HTML, CSS, and JavaScript, providing an intuitive interface for any user to get movie recommendations.

---

## 🔑 Key Features

- **Live Web Service**: The backend is deployed as a persistent web service on Render, making the ML model accessible to any client via its public API.
- **Machine Learning Model**: Implements a content-based filtering model using TF-IDF and Cosine Similarity to recommend movies based on genre.
- **RESTful API**: A custom API built with Flask to serve model predictions from a clean `/recommend` endpoint.
- **Interactive Frontend**: A clean user interface that allows users to input a movie and receive a list of recommendations fetched from the live backend service.

---

## 🧰 Built With

### Backend & Machine Learning:
- Python
- Flask
- Pandas
- Scikit-learn
- Gunicorn

### Frontend:
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)

### Deployment:
- Render (for the Python Web Service)

---

## ⚙️ Getting Started

### Prerequisites

You will need to have Python 3 and `pip` installed on your system.

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your_username/your_repository_name.git

# Navigate to the project directory
cd movie-recommender

# Create the virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Download the dataset:

Download the **ml-latest-small.zip** dataset from [MovieLens](https://grouplens.org/datasets/movielens/).

Unzip it and place the `movies.csv` and `ratings.csv` files in the root of the project folder.

---

## ▶️ Running the Application

```bash
# Start the development server
flask run --port=8080
```

Open your browser and navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080) to see the application in action.

---

## 🙏 Acknowledgments

- This project uses the **MovieLens** dataset, collected by the [GroupLens research group](https://grouplens.org) at the University of Minnesota.
- Web service hosting by [Render](https://render.com).
