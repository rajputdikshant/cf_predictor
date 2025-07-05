# cf_predictor

[Deatail overview of the project.pdf](https://github.com/user-attachments/files/20863100/Data_Mining_and_Analysis_Assingment.pdf)



# Codeforces Rank Predictor 🏆

A machine learning-powered web application that predicts your future Codeforces rank based on your current performance, activity patterns, and problem-solving history.

## 📋 Overview

This project uses advanced machine learning algorithms to analyze your Codeforces profile and predict your potential rank progression over different time periods (1 month, 2 months, or 1 year). The system considers multiple factors including your current rating, problem-solving patterns, contest participation, and topic expertise to provide accurate predictions.

## ✨ Features

- **🎯 Smart Rank Prediction**: Predicts your future Codeforces rank using machine learning models
- **📊 Interactive Visualizations**: Beautiful charts showing your rank progression over time
- **⏰ Multiple Timelines**: Choose between 1 month, 2 months, or 1 year predictions
- **📈 Historical Analysis**: Analyzes your past performance to understand growth patterns
- **🏷️ Topic Analysis**: Tracks your expertise across different algorithm topics
- **🎨 Modern UI**: Clean, responsive interface built with Bootstrap 5 and Chart.js
- **📱 Mobile Friendly**: Works seamlessly on desktop and mobile devices

## 🚀 How It Works

### 1. Data Collection
The application fetches your data from Codeforces API:
- **User Information**: Current rating, max rating, rank
- **Contest History**: All participated contests and ratings
- **Submission History**: All problem submissions and their verdicts
- **Problem Tags**: Algorithm topics you've solved

### 2. Feature Engineering
The system extracts meaningful features from your data:
- Current and maximum ratings
- Number of contests participated
- Total problems solved
- Topic-wise problem distribution (18 different algorithm topics)
- Activity patterns (problems per month, contests per month)

### 3. Machine Learning Prediction
The prediction model uses:
- **XGBoost Regression**: Trained on historical Codeforces data
- **Adaptive Growth Factors**: Different growth rates based on current rating level
- **Activity Bonuses**: Rewards for consistent problem-solving and contest participation
- **Topic Progression**: Simulates improvement in different algorithm areas

### 4. Rank Calculation
Predictions are mapped to Codeforces ranks:
- **Newbie**: 0-1199
- **Pupil**: 1200-1399
- **Specialist**: 1400-1599
- **Expert**: 1600-1899
- **Candidate Master**: 1900-2099
- **Master**: 2100-2299
- **International Master**: 2300-2399
- **Grandmaster**: 2400-2599
- **International Grandmaster**: 2600-2999
- **Legendary Grandmaster**: 3000+

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cf_predictor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 📦 Dependencies

The project uses the following key libraries:
- **Flask**: Web framework for the application
- **XGBoost**: Machine learning model for predictions
- **Pandas & NumPy**: Data manipulation and numerical computations
- **Requests**: API calls to Codeforces
- **Joblib**: Model serialization and loading
- **Bootstrap 5**: Frontend styling and components
- **Chart.js**: Interactive data visualizations

## 🎯 How to Use

1. **Enter Your Handle**: Type your Codeforces username in the input field
2. **Select Timeline**: Choose your desired prediction period (1 month, 2 months, or 1 year)
3. **Get Prediction**: Click "Predict My Rank" to analyze your profile
4. **View Results**: See your current rank, predicted rank, and progression chart
5. **Get Insights**: Review personalized improvement suggestions

## 🔧 Technical Architecture

### Backend (Python/Flask)
- **app.py**: Main Flask application with prediction logic
- **model.pkl**: Trained XGBoost model for rank prediction
- **model_features.pkl**: Feature names used by the model
- **rank_encoder.pkl**: Rank encoding for the model

### Frontend (HTML/CSS/JavaScript)
- **templates/index.html**: Main web interface
- **Bootstrap 5**: Responsive design framework
- **Chart.js**: Interactive data visualization
- **Font Awesome**: Icons and visual elements

### API Integration
- **Codeforces API**: Fetches user data, contest history, and submissions
- **Real-time Data**: Always uses the latest user information

## 📊 Algorithm Topics Covered

The system tracks your expertise in 18 different algorithm topics:
- Binary Search
- Bitmasks
- Brute Force
- Combinatorics
- Constructive Algorithms
- Data Structures
- DFS and Similar
- Dynamic Programming (DP)
- Disjoint Set Union (DSU)
- Games
- Graphs
- Greedy
- Implementation
- Math
- Number Theory
- Sortings
- Strings
- Trees

## 🎨 Features in Detail

### Adaptive Growth System
The prediction model uses different growth factors based on your current rating:
- **Newbies (<1200)**: Up to 40% growth potential
- **Pupils (1200-1399)**: Up to 30% growth potential
- **Specialists (1400-1599)**: Up to 22% growth potential
- **Experts (1600-1899)**: Up to 15% growth potential
- **Higher Ranks**: Diminishing growth rates for realistic predictions

### Activity Analysis
- **Problems per Month**: Calculates your average problem-solving rate
- **Contests per Month**: Tracks your contest participation frequency
- **Active Months**: Determines how long you've been active on Codeforces

### Historical Data Integration
- **Past 10 Contests**: Analyzes your recent performance trends
- **Rating Progression**: Shows your historical rating changes
- **Growth Patterns**: Identifies your improvement rate over time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Performance improvements
- Documentation updates

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Codeforces**: For providing the API and competitive programming platform
- **XGBoost**: For the powerful machine learning framework
- **Flask**: For the lightweight web framework
- **Bootstrap**: For the beautiful UI components
- **Chart.js**: For the interactive data visualizations

## 📞 Support

If you encounter any issues or have questions:
1. Check the existing issues in the repository
2. Create a new issue with detailed information
3. Include your Codeforces handle and the error message

---

**Happy Coding and Good Luck with Your Competitive Programming Journey! 🚀**

