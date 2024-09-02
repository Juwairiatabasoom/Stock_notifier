import requests
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_APIKEY="44d70b9761214f0e8b074e50c818fc1f"
STOCK_APIKEY="AO619A519FUJY6PO"

Stock_parameters={"function":"TIME_SERIES_DAILY","symbol":"TSLA","apikey":STOCK_APIKEY}
stock_response=requests.get(url=STOCK_ENDPOINT,params=Stock_parameters)
data=stock_response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]

#yesterday's closing value
yesterdays_data=data_list[0]
yesterdays_closing_value=yesterdays_data["4. close"]

#day before yesterday's closing value:

day_before_yesterday=data_list[1]
day_bef_yes_closing_value=day_before_yesterday["4. close"]

#difference:
difference=float(yesterdays_closing_value)-float(day_bef_yes_closing_value)

up_down=None
if difference>0:
    updown="🔺"
else:
    up_down="🔻"

#percentage:
percentage=round((difference/float(yesterdays_closing_value))*100)
print(percentage)

##News API
if abs(percentage)>1:
    params={"apiKey":NEWS_APIKEY,"q":"Tesla"}
    res=requests.get(url=NEWS_ENDPOINT,params=params)
    data=res.json()
    articles=data["articles"]
    three_articles=articles[:3]

    #list of three articles
    formatted_articles=[f"{STOCK_NAME} {updown}{percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python

    from twilio.rest import Client
    account_sid="ACa7bd58fef86180525a4087f650afe896"
    auth_token="28aec0a7a03aa613fdd983823b9744ad"
    client=Client(account_sid,auth_token)
    for article in formatted_articles:
        message=client.messages.create(body=article,from_="+14432143436",to="+918985988884")
