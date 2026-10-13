# VS2603-Fashion-Advisor
Transforms past purchases into an intelligent, privately curated digital closet. Describe your event, mood, or local weather, and the AI assembles complete, ready-to-wear looks from the pieces you already own. If your wardrobe is missing the right attire for an occasion, it instantly surfaces tailored store recommendations to complete the look.

Open VS Code, Enter the unzipped folder into VS Code and open the terminal then into the terminal paste: "python -m venv venv" ".\venv\Scripts\activate"

To use this, you need to get some libraries: So paste the following in your terminal: "pip install fastapi uvicorn openai pydantic"

LM Studio is used in this code, you can download it to host your own LLMs locally and use those in running this application. I recommend Mistral 7B models.
You can find tutorials online on how to install it, start a server etc.

Go into Terminal and paste, this starts the AI and it's processing:
'uvicorn main:app --reload'

You can view the app at:
http://127.0.0.1:8000

Wait for a few seconds, it is slightly heavy. Also, i have pasted all this because I am nervous about adding an .env file
