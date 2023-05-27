from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext, PromptHelper
from langchain import OpenAI
import discord
import os
from flask import Flask
from threading import Thread
from waitress import serve
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = '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'
os.environ["DISCORD_TOKEN_KEY"] = 'MTEwOTAwNjk4NTgyOTA0MDIxOA.GsJXlj.WkfhHE7CMkvHAeY58s0OOi2QgAl96qe2Hb8mT4'

app = Flask(__name__)

@app.route("/health")
def health_check():
    return "OK", 200

def run_flask_app():
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def run_discord_bot():
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("No DISCORD_BOT_TOKEN found in environment variables")

    # Start the Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    client.run(TOKEN)

def construct_index(directory_path):
    MAX_INPUT_SIZE = 4096
    MAX_OUTPUT_SIZE = 256 #512
    MAX_CHUCK_OVERLAP = 20

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    prompt_helper = PromptHelper(MAX_INPUT_SIZE, MAX_OUTPUT_SIZE, MAX_CHUCK_OVERLAP)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    docs = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex.from_documents(docs, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="detailed")
    return response.response

index = construct_index("docs")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    # Check if the bot is mentioned in the message
    if client.user in msg.mentions:
        index = GPTSimpleVectorIndex.load_from_disk('index.json')
        input_text = f"{msg.content}"
        response = index.query(input_text, response_mode="compact")
        # return response.response
        await msg.channel.send(response.response)

# TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if __name__ == "__main__":
    run_discord_bot()
    # client.run(os.environ["DISCORD_TOKEN_KEY"])