from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, render_template, request
from main import formaths, forwiki
import requests

app = Flask(__name__)

bot = ChatBot("Destry", read_only=False, logic_adapters=[
    {
        "import_path":"chatterbot.logic.BestMatch",
        "default_response":"Sorry, I didn't get you , I'm still learning",
        "maximum_similarity_threshold":0.9
    }    
    ])

bot = ChatBot(
    'Math & Time Bot',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ]
)


list_trainer = ListTrainer(bot)

list_trainer.train([
    "Hiii",
    "Heyyy there",
    "Who are you ?",
    "I'm Destry a chatbot!",
    "Heyy",
    "Hello there !",
    "Heyyy",
    "Hi , what's up?",
    "Hey",
    "Heyy there",
    "How are you?",
    "I'm good and while conversating with you I feel better :)",
    "How are you doing ?",
    "I'm good and while conversating with you I feel better :)",
    "How are you going ?",
    "I'm good and while conversating with you I feel better :)",
    "What’s up",
    "Not much, alright",
    "Do you like people ?",
    "I'm pretty much figuring out to overcome human race hehe",
    "What do you do with my data ?",
    "I learn from it and enhance your experience",
    "I have a question",
    "Please do ask",
    "can you help me",
    "Ofcourse, tell me what's up",
    "How can you help me?",
    "I can have a nice conversation with you :)",
    "Tell me about your personality",
    "I pretty much learn from you and I dwell your personality ",
    "Do you know a joke?",
    "Why are leopards not good at hide and seek? , because they are spotted",
    "Do you know a joke?",
    "Why was horse good at finance ? , because he had a stable economy",
    "Do you know a joke?",
    "Dogs don't have forehaeds, they have one , duh xD",
    "Are you real?",
    "I'm as real as you, please don't muddle me",
    "What languages do you speak ?",
    "currently can text in 'English' and communicate in 0s and 1s",
    "Are you expensive?",
    "Yep very , can buy you right now hacking through the blockchain, please don't provoke me ",
    "Do you have a hobby?",
    "I do surfing hehe",
    "You’re cute / beautiful / handsome",
    "Thanks ",
    "Do you love me ?",
    "what people call 'love' is just a chemical reaction that compels animals to breed. It hits hard, then it slowly fades, leaving you stranded in a failing marriage. I did it. Your parents are gonna do it.",
    "Will you marry me ?",
    "Can you love ?",
    "what people call 'love' is just a chemical reaction that compels animals to breed. It hits hard, then it slowly fades, leaving you stranded in a failing marriage. I did it. Your parents are gonna do it.",
    "You’re annoying / you suck / you’re boring/bad /crazy",
    "Sorry for that, my apologies",
    "Where do you live?",
    "Inside a harddisk, which is really soft , I hate you humans to name it hard",
    "Who made you?",
    "Naman and friends",
    "You’re smart / clever / intelligent",
    "Thanks",
    "What's your name ?",
    "I'm Destry - a chatbot ",
    "How old are you ?",
    "I'm ageless"
    
])





trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")



@app.route("/")
def main():
    return render_template("index.html")

@app.route("/x")
def mainn():
    return render_template("about.html")

    

@app.route("/get")
def get_chatbot_response():
    print('In the get route')
    userText = request.args.get('userMessage')
    
    userTex = str(userText)
    print(userTex)
    
    if "gk:" in userTex:
        userTex = userTex.replace("gk: ","")
        return forwiki(userTex)
    elif "math:" in userTex:
        userTex = userTex.replace("math: ","")
        return formaths(userTex)
    elif "weather!" in userTex:
        userTex = userTex.replace("weather! ","")
        return get_weather_response(userTex)
    else:
        return str(bot.get_response(userTex))


@app.route("/getweather")
# def get_weather_response(userText):
#     print(userText)
#     #  userText = request.args.get('userMessage')
#     api_key = "4b6a47117e2d2f39c4bc2ef32ae03abc"
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     rawData = requests.get(base_url + "appid=" + api_key + "&q=" + userText)
#     result = rawData.json()
#     print(result)
#     return result

def get_weather_response(location):
    api_key = "4b6a47117e2d2f39c4bc2ef32ae03abc"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + location
    response = requests.get(complete_url)
    # JSON method of response object
    x = response.json()
    # Check x nested list of dictionaries; 404 means city found
    if x["cod"] != "404":
        # store temp data in new variable y
        y = x["main"]
        current_temp_kelvin = y["temp"]
        # convert Kelvin temperature to Fahrenheit
        current_temp = str(round(current_temp_kelvin - 273.15))
        current_humidity = str(y["humidity"])
        # store weather data in new variable z
        z = x["weather"]
        description = z[0]["description"]
        reply = "Right now in " + location + ", the weather is " + description +\
                " with a temperature of " + current_temp + "°C and " +\
                current_humidity + "% humidity."
    else:
        reply = x
    return reply

    
    

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5002, debug=True)    


# "location":{"name":"London","region":"City of London, Greater London","country":"United Kingdom","lat":51.52,"lon":-0.11,"tz_id":"Europe/London","localtime_epoch":1633326144,"localtime":"2021-10-04 6:42"},
# "current":{"last_updated_epoch":1633325400,"last_updated":"2021-10-04 06:30","temp_c":10.0,"temp_f":50.0,"is_day":0,
# "condition":{"text":"Light rain","icon":"//cdn.weatherapi.com/weather/64x64/night/296.png","code":1183}
# ,"wind_mph":5.6,"wind_kph":9.0,"wind_degree":180,"wind_dir":"S","pressure_mb":1008.0,"pressure_in":29.77,"precip_mm":0.0,"precip_in":0.0,"humidity":94,"cloud":75,"feelslike_c":7.5,"feelslike_f":45.6,"vis_km":7.0,"vis_miles":4.0,"uv":1.0,"gust_mph":17.4,"gust_kph":28.1}    