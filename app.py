from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import numpy as np
import joblib
import json
import math
from datetime import datetime

app = Flask(__name__)

# Mapping timeline values to labels
TL_MAP = {
    '30': '1 Month',
    '60': '2 Months',
    '365': '1 Year'
}

# Load the regression model
model = joblib.load('model.pkl')

# Define rank thresholds for Codeforces
RANK_THRESHOLDS = {
    'Newbie': [0, 1199],
    'Pupil': [1200, 1399],
    'Specialist': [1400, 1599],
    'Expert': [1600, 1899],
    'Candidate Master': [1900, 2099],
    'Master': [2100, 2299],
    'International Master': [2300, 2399],
    'Grandmaster': [2400, 2599],
    'International Grandmaster': [2600, 2999],
    'Legendary Grandmaster': [3000, 9999]
}

def get_rank_from_rating(rating):
    if rating is None or np.isnan(rating):
        return 'Unrated'
    for rank, (low, high) in RANK_THRESHOLDS.items():
        if low <= rating <= high:
            return rank
    return 'Unrated'

TOPICS = [
    'binary search', 'bitmasks', 'brute force', 'combinatorics',
    'constructive algorithms', 'data structures', 'dfs and similar',
    'dp', 'dsu', 'games', 'graphs', 'greedy', 'implementation',
    'math', 'number theory', 'sortings', 'strings', 'trees'
]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def calculate_activity(submissions, contests):
    if not submissions:
        return {}
    submission_dates = [datetime.fromtimestamp(s['creationTimeSeconds']) for s in submissions]
    first_sub = min(submission_dates)
    last_sub = max(submission_dates)
    months_active = (last_sub.year - first_sub.year) * 12 + (last_sub.month - first_sub.month) + 1
    return {
        'problems_per_month': len(submissions) / months_active if months_active > 0 else 0,
        'contests_per_month': len(contests) / months_active if months_active > 0 else 0,
        'active_months': months_active
    }

@app.route('/predict', methods=['POST'])
def predict():
    handle = request.form['handle'].strip()
    timeline = request.form['timeline']
    days = int(timeline)
    
    try:
        info_r = requests.get(f'https://codeforces.com/api/user.info?handles={handle}').json()
        if info_r.get('status') != 'OK':
            return render_template('index.html', error="Handle not found.")
        info = info_r['result'][0]
    except Exception as e:
        return render_template('index.html', error=f"Error fetching user data: {str(e)}")

    try:
        rating_r = requests.get(f'https://codeforces.com/api/user.rating?handle={handle}').json()
        contests = rating_r.get('result', [])
    except Exception:
        contests = []

    try:
        subs_r = requests.get(f'https://codeforces.com/api/user.status?handle={handle}&from=1&count=100000').json()
        submissions = subs_r.get('result', [])
    except Exception:
        submissions = []

    solved = set()
    tag_counts = {t: 0 for t in TOPICS}

    for sub in submissions:
        if sub.get('verdict') == 'OK':
            problem = sub['problem']
            pid = (problem.get('contestId', 0), problem.get('index', ''))
            if pid not in solved:
                solved.add(pid)
                for tag in problem.get('tags', []):
                    if tag in tag_counts:
                        tag_counts[tag] += 1

    current_rating = info.get('rating', 0)
    max_rating = info.get('maxRating', 0)
    current_rank = get_rank_from_rating(current_rating)

    base_features = {
        'user_summary_current_rating': current_rating,
        'user_summary_max_rating': max_rating,
        'user_summary_contests_participated': len(contests),
        'user_summary_problems_solved_count': len(solved),
    }

    for t in TOPICS:
        base_features[f'topic_{t.replace(" ", "_")}'] = tag_counts.get(t, 0)

    try:
        model_features = joblib.load('model_features.pkl')
    except:
        return render_template('index.html', error="Model features not found.")

    activity = calculate_activity(submissions, contests)
    
    predictions = []
    ranks = []
    rank_indices = []
    rank_order = ['Unrated'] + list(RANK_THRESHOLDS.keys())

    days_list = []
    if days <= 30:
        days_list = [0, 7, 15, 30]
    elif days <= 60:
        days_list = [0, 15, 30, 45, 60]
    else:
        days_list = [0, 30, 60, 120, 180, 270, 365]

    prev_rating = current_rating
    prev_max = max_rating
    prev_problems = len(solved)
    prev_contests = len(contests)

    for i, day in enumerate(days_list):
        if day == 0:
            predicted_rating = current_rating
            features = base_features.copy()
        else:
            features = base_features.copy()
            features['user_summary_current_rating'] = prev_rating
            features['user_summary_max_rating'] = max(prev_max, prev_rating)

            # Simulate contest participation: scale with time, not capped at 1
            contest_increment = max(1, int((day / 30) * max(1, activity.get('contests_per_month', 2))))
            features['user_summary_contests_participated'] = prev_contests + contest_increment

            # Simulate problem solving: scale with time, not capped
            problem_increment = max(1, int((day / 30) * max(1, activity.get('problems_per_month', 30))))
            features['user_summary_problems_solved_count'] = prev_problems + problem_increment

            # Simulate topic progression
            total_topics = sum(tag_counts.values())
            if total_topics > 0:
                for topic in TOPICS:
                    key = f'topic_{topic.replace(" ", "_")}'
                    current = tag_counts.get(topic, 0)
                    proportion = current / total_topics
                    features[key] = current + int(problem_increment * proportion)
            else:
                for topic in TOPICS:
                    key = f'topic_{topic.replace(" ", "_")}'
                    features[key] = features.get(key, 0) + int(problem_increment / len(TOPICS))

            # Prepare prediction input
            X_pred = pd.DataFrame([features]).reindex(columns=model_features, fill_value=0)

            # Get model prediction
            raw_prediction = float(model.predict(X_pred)[0])

            # Calculate progress percentage
            progress = day / days

            # --- ADAPTIVE GROWTH FOR HIGHER RATINGS ---
            # The higher the rating, the harder it is to grow
            # Use a diminishing growth factor based on current rating
            # E.g., above 2100, growth is much slower; above 2400, even slower
            if prev_rating < 1200:
                max_growth_factor = 0.40  # up to 40% for newbies
            elif prev_rating < 1600:
                max_growth_factor = 0.30
            elif prev_rating < 1900:
                max_growth_factor = 0.22
            elif prev_rating < 2100:
                max_growth_factor = 0.15
            elif prev_rating < 2400:
                max_growth_factor = 0.08
            elif prev_rating < 3000:
                max_growth_factor = 0.04
            else:
                max_growth_factor = 0.02

            base_growth = current_rating * max_growth_factor * progress
            activity_bonus = math.log(problem_increment + 1) * (10 * max_growth_factor)
            contest_bonus = contest_increment * (15 * max_growth_factor)

            predicted_rating = raw_prediction + activity_bonus + contest_bonus
            min_rating = prev_rating + (base_growth * 0.5)
            max_rating_progress = current_rating + (current_rating * max_growth_factor) * progress

            predicted_rating = max(min_rating, min(max_rating_progress, predicted_rating))
            predicted_rating = max(prev_rating * (1 + 0.003 * max_growth_factor), predicted_rating)  # Ensure at least a little growth

        predictions.append(predicted_rating)
        rank = get_rank_from_rating(predicted_rating)
        ranks.append(rank)
        rank_indices.append(rank_order.index(rank) if rank in rank_order else 0)

        prev_rating = predicted_rating
        prev_max = max(prev_max, predicted_rating)
        prev_problems = features.get('user_summary_problems_solved_count', prev_problems)
        prev_contests = features.get('user_summary_contests_participated', prev_contests)

    # Historical data processing
    historical_ratings = []
    historical_days = []
    historical_ranks = []
    historical_indices = []

    if contests:
        sorted_contests = sorted(contests, key=lambda x: x['ratingUpdateTimeSeconds'])
        latest_time = sorted_contests[-1]['ratingUpdateTimeSeconds']
        for contest in sorted_contests[-10:]:
            days_diff = -int((latest_time - contest['ratingUpdateTimeSeconds']) / 86400)
            historical_days.append(days_diff)
            rating = contest.get('newRating', 0)
            historical_ratings.append(rating)
            rank = get_rank_from_rating(rating)
            historical_ranks.append(rank)
            historical_indices.append(rank_order.index(rank) if rank in rank_order else 0)

    return render_template('index.html',
                         handle=handle,
                         current_rank=current_rank,
                         current_rating=current_rating,
                         prediction=ranks[-1],
                         timeline=TL_MAP.get(timeline, f'{timeline} days'),
                         timeline_days=days,
                         days_json=json.dumps(days_list),
                         predictions_json=json.dumps(predictions),
                         ranks_json=json.dumps(ranks),
                         rank_indices_json=json.dumps(rank_indices),
                         historical_days_json=json.dumps(historical_days),
                         historical_ratings_json=json.dumps(historical_ratings),
                         historical_ranks_json=json.dumps(historical_ranks),
                         historical_indices_json=json.dumps(historical_indices))

if __name__ == '__main__':
    app.run(debug=True)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
