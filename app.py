from flask import Flask, request, jsonify, render_template
import re
import requests
import hashlib

app = Flask(__name__)

COMMON_PASSWORDS = {
    'password', '123456', '123456789', '12345678', '12345', 'qwerty', 'abc123',
    'football', 'monkey', 'letmein', 'shadow', 'master', '666666', '123123'
}

def check_password_leak(password):
    """
    Use Have I Been Pwned API to check if password is leaked.
    Returns number of times it was found or 0 if not found.
    """
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    res = requests.get(url)
    if res.status_code != 200:
        return 0  # Cannot check, assume safe

    hashes = (line.split(':') for line in res.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def estimate_crack_time(password):
    length = len(password)
    variety = 0
    if re.search(r'[a-z]', password): variety += 26
    if re.search(r'[A-Z]', password): variety += 26
    if re.search(r'[0-9]', password): variety += 10
    if re.search(r'[^A-Za-z0-9]', password): variety += 32

    if variety == 0:
        return "Instantly"

    combinations = variety ** length
    guesses_per_second = 1e10  # 10 billion guesses per second, rough estimate

    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        years = seconds / 31536000
        return f"{years:.1f} years"

def get_suggestions(password):
    suggestions = []
    if len(password) < 12:
        suggestions.append("Use at least 12 characters")
    if not re.search(r'[a-z]', password):
        suggestions.append("Add lowercase letters")
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add uppercase letters")
    if not re.search(r'[0-9]', password):
        suggestions.append("Add numbers")
    if not re.search(r'[^A-Za-z0-9]', password):
        suggestions.append("Add special characters")
    if password.lower() in COMMON_PASSWORDS:
        suggestions.insert(0, "Your password is too common!")
    leak_count = check_password_leak(password)
    if leak_count > 0:
        suggestions.insert(0, f"Password found {leak_count} times in data breaches!")
    return suggestions

def password_strength(password):
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[^A-Za-z0-9]', password):
        score += 2

    if score <= 3:
        return "Weak"
    elif score <= 5:
        return "Moderate"
    else:
        return "Strong"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    password = data.get('password', '')

    strength = password_strength(password)
    crack_time = estimate_crack_time(password)
    suggestions = get_suggestions(password)

    return jsonify({
        'strength': strength,
        'crack_time': crack_time,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)