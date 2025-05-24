Password Strength Analyzer
## Overview:
Password Strength Analyzer is a web application that helps user evaluate the strength of their password
in real time. It analyzes various factors such as length, character variety and checks against common
passwords and known data breaches to provide actionable feedback to create strong passwords.

## Features:
- Real time password evaluation (weak, moderate, strong).
- Visual Strength meter.
- Criteria checked list
- Estimated crack time calculation.
- Common password detection.
- Integrated with "Have I been pwned" API to check password leaks.
- Show/hide password toggle.
- Light and dark mode support.
- Clean and minimal responsive UI.

## Technologies used:
- Frontend: HTML, CSS, JS
- Backend: Python3, flask framework.
- External library: requests for API calls.
- API: Have I been pwned for password leaks.

## Installation:
## Clone the repository
git clone https://github.com/droid-create/password-strength-analyzer.git
cd password-strength-analyzer

## Create and activate virtual environment
python -m venv pass //creates virtual environment named pass
pass/Scripts/activate // activates virtual environment

## Install dependencies
pip install -r requirements.txt  // installs Flask and requests //

## if requirements file does not work.
python -m pip install flask
python -m pip install requests

## Run the app
python app.py

Open your browser and go to https://127.0.0.1:5000

## To re-run this project
.\pass\Scripts/activate
python app.py

Usage:
- Enter password into input field.
- Valid real time strength, crack time estimation and suggestion.
- Toggle password visibility using checkbox.
- Switch between light and dark mode.

Future Scope:
- Multi language support.
- User authentication.
- integration with browser extension/
- ML based strength prediction.
- Password generator.
- Export and creating reports feature.

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this project for personal or commercial use, as long as you include proper attribution.
