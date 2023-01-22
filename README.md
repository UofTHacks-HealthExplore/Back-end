# Back-end

using python3.9 (although other versions should be fine)

```
python -m venv venv  # install the virtual environment
venv\scripts\activate  # activate the virtual environment
pip install -r requirements.txt  # install requirements.txt inside of the virtual environment
.env file includes API key for openai
python chatbot.py  # run the program
```

create an openai account -> api key is free
create a .env file in the same level as `chatbot.py` with the contents
```env
OPENAI_API_KEY = "<key in quotes>"
```

This repository contains the files to the two openai chat bots we are using for our simulation

### How to use the backend
Instructions found in `home.html` when booting up the app.

### Setting up on [pythonanywhere.com](https://www.pythonanywhere.com/)
This is the best alternative we could find to Heroku thats bot lightweight and easy to set up.

Setup notes:
```
- .env in /home/<user>
- templates folder in /home/<user>/mysite
- contents of chatbot.py in /home/kevinzwang5129/mysite/flask_app.py
- virtualenv in /home/<user>/.virtualenvs/hackuoft
```
Important things to note:
- Python version and virtualenv versions are the same
- Information about error logs (and basically everything else) may be found on the "web" tab
