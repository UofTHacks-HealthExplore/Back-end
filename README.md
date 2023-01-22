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
