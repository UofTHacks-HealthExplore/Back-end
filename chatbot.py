import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for
from random import choice


app = Flask(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

chat = [("AI", "How are you feeling?")]
choices = [None]*5
personalized = ""


def format_dialogue(dialogue):
    """
    formats it this manner:
    - no trailing whitespace
    - no leading whitespace

    -----
    |AI: <text>
    |Me: <text>
    |AI: <text>
    ...
    |Me: <text>
    ----
    """
    formatted = ""

    for user, dial in dialogue:
        # Might be the case that dialogue might have trailing whitespace
        dial = dial.strip()

        formatted += f"{user}: {dial}\n"

    return formatted.strip()


def model_gen_user_responses(dialogue):
    """
    `dialogue` is a an array of tuples

    formatted string used for gpt-3 query is
    -----
    |AI: <text>
    ...
    |AI: <text>
    |query
    -----
    """

    formatted = format_dialogue(dialogue)

    # For generating 5 possible responses
    query = "Generate five possible responses that the human can respond with given the previous chat. Keep the topic on mental health:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{formatted}\n{query}",
        temperature=0.6,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    tmp_choices = response["choices"][0]["text"]  # Get the actual text as raw string
    choices_list = tmp_choices.strip().split("\n")  # List of 5 choices

    for i, val in enumerate(choices_list):
        # Removing the "1. " prefix
        # Stripping incase of whitespace characters
        choices[i] = val[3:].strip()

    return choices_list  # Returns properly formatted


def write_user_select_response(selection):
    """
    `choices_list` is a list of responses with properly formatted text
    """

    # Will always be 5 choices
    # Selection will be an integer from 1 to 5
    selected = choices[selection-1]
    chat.append(("Me", selected))
    return selected


def model_gen_ai_response(chat):
    """
    generates the ai response after you pick a response
    """
    formatted = format_dialogue(chat)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{formatted}\nAI: ",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    # Get the actual text as raw string
    choice = response["choices"][0]["text"].strip()
    chat.append(("AI", choice))


def model_gen_tips(chat):
    """
    generates a random tip
    """

    formatted = format_dialogue(chat)

    query = "Based on the previous chat, provide a mental health tip for the user"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{formatted}\n{query}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    # Assuming in the format of 1. 2. 3. 4. 5.

    tmp_choices = response["choices"][0]["text"].strip()  # Get
    return tmp_choices


def model_gen_articles(chat):
    """
    generates a random article, video, therapy group
    """

    """
    generates a random tip
    """

    formatted = format_dialogue(chat)
    tys = ["article", "video", "therapy group", "psychology group"]

    query = f"Based on the previous chat, provide a link to a {choice(tys)} related to mental health for the user:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{formatted}\n{query}",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    # Assuming in the format of 1. 2. 3. 4. 5.

    tmp_choices = response["choices"][0]["text"].strip()  # Get the actual text as raw string
    return tmp_choices


def model_gen_personalized(chat):
    """
    generates a random personalized resource when entering phase 3 (need a bit more location information)
    """

    formatted = format_dialogue(chat)

    query = f"Based on the previous chat and the new information (user is studying at waterloo, undergrad, not living on residence, long commute, hard to get work done), link one mental health resource for the user:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{formatted}\n{query}",
        temperature=0.9,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6
    )

    # Assuming in the format of 1. 2. 3. 4. 5.

    tmp_choices = response["choices"][0]["text"].strip()  # Get the actual text as raw string
    return tmp_choices


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/reset")
def reset():
    chat = [("AI", "How are you feeling?")]
    choices = [None]*5
    personalized = ""
    return render_template("home.html")


@app.route('/test')
def test():
    return render_template("redirect.html")


@app.route("/send_personalized")
def send_personalized():
    global personalized
    res = request.args.get("q")
    personalized = res
    return res


@app.route("/gen_personalized")
def gen_personalized():
    return model_gen_personalized(chat)


@app.route("/gen_articles")
def gen_articles():
    return model_gen_articles(chat)


@app.route("/gen_tips")
def gen_tips():
    return model_gen_tips(chat)


@app.route("/chatlog")
def chatlog():
    return format_dialogue(chat)


@app.route("/last_question")
def last_question():
    """
    return the last question that the AI asks
    """
    return chat[-1][1]


@app.route("/gen_responses")
def gen_responses():
    model_gen_user_responses(chat)
    return "generated"


@app.route("/responses/all")
def responses():
    return choices


@app.route("/responses/<int:sel>")
def select(sel):
    return choices[sel-1]


@app.route("/responses/<int:sel>/send")
def write(sel):
    write_user_select_response(sel)
    model_gen_ai_response(chat)
    return "sent!"


if __name__ == "__main__":
    # for i in range(3):
    #     print(format_dialogue(chat))
    #     choices = model_gen_user_responses(chat)
    #     print("-----")
    #     for i, ii in enumerate(choices, start=1):
    #         print(i, ii)
    #     print("-----")
    #     sel = int(input("ayo which one [1-5]: "))

    #     write_user_select_response(choices, sel)
    #     model_gen_ai_response(chat)

    app.run(debug=True)