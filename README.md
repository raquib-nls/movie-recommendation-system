# 🎬 Movie Recommendation System

A machine learning-based movie recommendation system that uses content-based filtering to suggest similar movies based on user preferences.

## 📋 Overview

This project implements a movie recommendation engine using cosine similarity and CountVectorizer to analyze movie features and generate personalized recommendations. The system processes movie metadata to create feature tags and finds similar movies based on content similarity.

## ✨ Features

- **Content-Based Filtering**: Uses movie metadata (genres, cast, crew, keywords) to recommend similar movies
- **Cosine Similarity**: Measures similarity between movies based on feature vectors
- **Efficient Processing**: Pre-computed similarity matrices stored as pickle files for fast recommendations
- **Movie Posters**: Fetches and displays high-quality movie posters using TMDB API
- **Trailer Integration**: Watch movie trailers directly with a dedicated trailer button for each recommendation
- **Smart Matching**: Matches movies using TMDB movie ID from the dataset, with fallback to title and release year for better accuracy
- **Sequel Detection**: Additional functionality to identify movie sequels (can be integrated separately)
- **Interactive UI**: Streamlit-based web interface for easy interaction

## 🛠️ Tech Stack

- **Python 3.x**
- **Machine Learning**: Scikit-learn (CountVectorizer, Cosine Similarity)
- **Data Processing**: Pandas, NumPy
- **Web Framework**: Streamlit
- **API Integration**: TMDB API (for posters and trailers)
- **Dataset**: TMDB 5000 Movies Dataset

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <[repo-url](https://github.com/raquib-nls/movie-recommendation-system.git)>
cd movie-recommendation-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download Pre-trained Models (Automatic)

The application will automatically download the required pickle files on first run:
- `movie_dict.pkl`
- `similarity.pkl`

**Google Drive Links** are embedded in `app.py`. These files will be downloaded only once and stored locally.

### 4. Download Dataset from Kaggle

Download the TMDB 5000 Movie Dataset from Kaggle:
- Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Required files:
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`

Place both CSV files in the project root directory or a `data/` folder.

### 5. Setup TMDB API Key

1. Create a free account on [TMDB](https://www.themoviedb.org/)
2. Navigate to Settings → API → Create API Key
3. Create a `.env` file in the project root or add your API key directly to `app.py`:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

This API key is used to fetch movie posters and trailer links.

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The web interface will open in your browser where you can:
1. Select a movie from the dropdown
2. View movie poster and access the trailer button
3. Get personalized movie recommendations with posters
4. Watch trailers for recommended movies

### Training the Model (Optional)

If you want to retrain the model or modify the feature engineering:

1. Open the Jupyter notebook provided in the repository
2. Load the TMDB datasets (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`)
3. Follow the notebook cells to:
   - Process and clean the data
   - Create feature tags using genres, keywords, cast, and crew
   - Apply CountVectorizer to convert tags into feature vectors
   - Compute cosine similarity matrix
   - Save the processed data as pickle files

## 📊 How It Works

1. **Data Preprocessing**: Combines movie and credits datasets, extracts relevant features
2. **Feature Engineering**: Creates unified tags from genres, keywords, cast, director information
3. **Vectorization**: Uses CountVectorizer to convert text tags into numerical vectors
4. **Similarity Calculation**: Computes cosine similarity between all movie vectors
5. **Recommendation**: Returns top N most similar movies based on similarity scores

## 🎯 Additional Features

### Sequel Detection Function

The project includes an **extra function for detecting movie sequels** that is not currently integrated into the UI. 

**Use Case**: You can create separate sections in the UI:
- **Similar Movies**: Based on content similarity
- **Sequel Movies**: Based on sequel detection algorithm

This allows users to explore both similar movies and official sequels/prequels in different sections.

## 🎥 Demo

[[Click Here !! (App)](https://cinepolis-movie-recmend-model.streamlit.app/)]

## 📁 Project Structure

```
movie-recommendation-system/
│
├── app.py                          # Main Streamlit application
├── movie_recommendation.ipynb      # Jupyter notebook for model training
├── requirements.txt                # Python dependencies
├── movie_dict.pkl                  # Preprocessed movie data (auto-downloaded)
├── similarity.pkl                  # Similarity matrix (auto-downloaded)
│
├── data/                           # Dataset folder (create this)
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── README.md                       # Project documentation
```

## 🔧 Customization

- **Modify Features**: Edit the notebook to include/exclude different movie features
- **Adjust Recommendations**: Change the number of recommendations returned
- **Add Sequel Section**: Integrate the sequel detection function into the UI
- **Enhance UI**: Customize the Streamlit interface with movie posters, ratings, etc.

## 📝 Requirements

```
pandas
numpy
scikit-learn
streamlit
requests
gdown
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Mohd Raquib Hussain

## 🙏 Acknowledgments

- TMDB for providing the movie dataset
- Kaggle for hosting the dataset
- Streamlit for the web framework

---

**Note**: Make sure to download the datasets from Kaggle before running the training notebook. The pickle files will be automatically downloaded when you run the app for the first time.


