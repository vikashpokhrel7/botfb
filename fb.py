from fbchat import Client, log, _graphql
from fbchat.models import *
import json
import random
import wolframalpha
import requests
import time
import math
import sqlite3
import os
import concurrent.futures
from difflib import SequenceMatcher, get_close_matches
# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
options = Options()
c = DesiredCapabilities.CHROME
c["pageLoadStrategy"] = "none"
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")



driver = webdriver.Chrome(
    service=Service(os.environ.get("CHROMEDRIVER_PATH")),
                    options=options, desired_capabilities=c)

class ChatBot(Client):

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg=str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg=(message_object.text).lower()
            except:
                pass

        def sendMsg():
            if (author_id != self.uid):
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        def sendQuery():
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        if(author_id == self.uid):
            pass
        else:
            try:
                conn=sqlite3.connect("messages.db")
                c=conn.cursor()
                c.execute("""
                CREATE TABLE IF NOT EXISTS "{}" (
                    mid text PRIMARY KEY,
                    message text NOT NULL
                );

                """.format(str(author_id).replace('"', '""')))

                c.execute("""

                INSERT INTO "{}" VALUES (?, ?)

                """.format(str(author_id).replace('"', '""')), (str(mid), msg))
                conn.commit()
                conn.close()
            except:
                pass

        def corona_details(country_name):
            from datetime import date, timedelta
            today=date.today()
            today=date.today()
            yesterday=today - timedelta(days=1)

            url="https://covid-193.p.rapidapi.com/history"

            querystring={"country": country_name, "day": yesterday}

            headers={
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66",
                'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }

            response=requests.request(
                "GET", url, headers=headers, params=querystring)
            data_str=response.text
            print(data_str)
            data=eval(data_str.replace("null", "None"))
            country=data["response"][0]["country"]
            new_cases=data["response"][0]["cases"]["new"]
            active_cases=data["response"][0]["cases"]["active"]
            total_cases=data["response"][0]["cases"]["total"]
            critical_cases=data["response"][0]["cases"]["critical"]
            total_deaths=data["response"][0]["deaths"]["total"]
            total_recovered=data["response"][0]["cases"]["recovered"]
            new_deaths=data["response"][0]["deaths"]["new"]
            reply=f'new cases: {new_cases}\n new_cases1 = {new_cases.replace("+", "")}\nnew_deaths1 = {new_deaths.replace("+", "")}\nactive cases: {active_cases}\nnew deaths: {new_deaths} total deaths: {total_deaths} \ncritical cases: {critical_cases}\ntotal cases: {total_cases}\ntotal recovered: {total_recovered}'
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

        def weather(city):
            api_address="https://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
            url=api_address + city
            json_data=requests.get(url).json()
            kelvin_res=json_data["main"]["temp"]
            feels_like=json_data["main"]["feels_like"]
            description=json_data["weather"][0]["description"]
            celcius_res=kelvin_res - 273.15
            max_temp=json_data["main"]["temp_max"]
            min_temp=json_data["main"]["temp_min"]
            visibility=json_data["visibility"]
            pressure=json_data["main"]["pressure"]
            humidity=json_data["main"]["humidity"]
            wind_speed=json_data["wind"]["speed"]
            print(
                f"maximum temperature: {max_temp-273.15} *C \nminimum temperature: {min_temp-273.15} *C")
            print(f"visibilty: {visibility}m")
            print(f"pressure: {pressure}")
            print(f"humidity: {humidity}")
            print(f"wind speed: {wind_speed}m/s")
            return(
                f"The current temperature of {city} is %.1f degree celcius with {description}" % celcius_res)



        def stepWiseCalculus(query):
            query=query.replace("+", "%2B")
            try:
                try:
                    api_address=f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
                    json_data=requests.get(api_address).json()
                    answer=json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
                    answer=answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                except:
                    pass
                try:
                    api_address=f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
                    json_data=requests.get(api_address).json()
                    answer=json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
                    answer=answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                except:
                    try:
                        answer=json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                        answer=answer.replace("sqrt", "√")

                        if(thread_type == ThreadType.USER):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                        elif(thread_type == ThreadType.GROUP):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                    except:
                        pass
            except:
                pass

        def stepWiseAlgebra(query):
            query=query.replace("+", "%2B")
            api_address=f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input=solve%203x^2+4x-6=0&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data=requests.get(api_address).json()
            try:
                answer=json_data["queryresult"]["pods"][1]["subpods"][2]["plaintext"]
                answer=answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer=json_data["queryresult"]["pods"][1]["subpods"][3]["plaintext"]
                answer=answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer=json_data["queryresult"]["pods"][1]["subpods"][4]["plaintext"]
                answer=answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer=json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                answer=answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer=json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                answer=answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass

        def stepWiseQueries(query):
            query=query.replace("+", "%2B")
            api_address=f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data=requests.get(api_address).json()
            try:
                try:
                    answer=json_data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                    answer=answer.replace("sqrt", "√")
                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer=json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                    answer=answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer=json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                    answer=answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
            except:
                self.send(Message(text="Cannot find the solution of this problem"), thread_id=thread_id,
                          thread_type=thread_type)

        try:
            def searchForUsers(self, name=" ".join(msg.split()[2:4]), limit=10):
                try:
                    limit=int(msg.split()[4])
                except:
                    limit=10
                params={"search": name, "limit": limit}
                (j,)=self.graphql_requests(
                    _graphql.from_query(_graphql.SEARCH_USER, params))
                users=([User._from_graphql(node)
                        for node in j[name]["users"]["nodes"]])
                for user in users:
                    reply=f"{user.name} profile_link: {user.url}\n friend: {user.is_friend}\n"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
        except:
            pass

        def programming_solution(self, query):
            try:
                count=int(msg.split()[-1])
            except:
                count=6
            try:
                x=int(query.split()[-1])
                if type(x) == int:
                    query=" ".join(msg.split()[0:-1])
            except:
                pass
            image_urls=[]

            url="https://bing-image-search1.p.rapidapi.com/images/search"

            querystring={"q": query, "count": str(count)}

            headers={
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
    }
            response=requests.request(
                "GET", url, headers=headers, params=querystring)
            data=json.loads(response.text)
            img_contents=(data["value"])
            # print(img_contents)
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def translator(self, query, target):
            query=" ".join(query.split()[1:-2])
            url="https://microsoft-translator-text.p.rapidapi.com/translate"

            querystring={"to": target, "api-version": "3.0",
                         "profanityAction": "NoAction", "textType": "plain"}

            payload=f'[{{"Text": "{query}"}}]'
            print("PAYLOAD>>", payload)
            headers={
                'content-type': "application/json",
                'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
    }

            response=requests.request(
                "POST", url, data=payload, headers=headers, params=querystring)

            json_response=eval(response.text)
            print(json_response[0]["translations"][0]["text"])
            print(json_response)
            return json_response[0]["translations"][0]["text"]

        def imageSearch(self, msg):
            try:
                count=int(msg.split()[-1])
            except:
                count=10
            query=" ".join(msg.split()[2:])
            try:
                x=int(query.split()[-1])
                if type(x) == int:
                    query=" ".join(msg.split()[2:-1])
            except:
                pass
            image_urls=[]

            url="https://bing-image-search1.p.rapidapi.com/images/search"

            querystring={"q": query, "count": str(count)}

            headers={
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
    }
            print("sending requests...")
            response=requests.request(
                "GET", url, headers=headers, params=querystring)
            print("got response..")
            data=json.loads(response.text)
            img_contents=(data["value"])
            # print(img_contents)
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def searchFiles(self):
            query=" ".join(msg.split()[2:])
            file_urls=[]
            url="https://filepursuit.p.rapidapi.com/"

            querystring={"q": query, "filetype": msg.split()[1]}

            headers={
                'x-rapidapi-host': "filepursuit.p.rapidapi.com",
                'x-rapidapi-key': "55d459414fmsh32c0a06c0e3e34dp1f40a5jsn084fca18f5ea"
    }

            response=requests.request(
                "GET", url, headers=headers, params=querystring)

            response=json.loads(response.text)
            file_contents=response["files_found"]
            try:
                for file in random.sample(file_contents, 10):
                    file_url=file["file_link"]
                    file_name=file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)
            except:
                for file in file_contents:
                    file_url=file["file_link"]
                    file_name=file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)


        try:
            if("search pdf" in msg):
                searchFiles(self)
            elif("check ipo" in msg):
                query=msg.split()
                company=" ".join(query[2:-1])
                if (company.split()[0]) == "of":
                    company=" ".join(query[3:-1])
                demat_num=int(query[-1])
                print("getting url")
                driver.get("https://iporesult.cdsc.com.np/")

                inp=driver.find_element(By.ID, "boid").send_keys(demat_num)

                companies=[]
                print("finding elements..")
                company_names=driver.find_element(
                    By.NAME,  "companyShare").find_elements(By.TAG_NAME, "option")
                for name in company_names:
                    companies.append(name.text)

                for full_comapany_name in companies[1:]:
                    print("inside loop..")
                    if(company) in full_comapany_name.lower():

                        select=Select(driver.find_element(
                            By.NAME, 'companyShare'))
                        select.select_by_visible_text(full_comapany_name)
                WebDriverWait(driver, 1).until(EC.invisibility_of_element(
                    (By.CSS_SELECTOR, "p-4.ng-touched.ng-dirty.ng-valid")))
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.mt-3.btn-block.w-100"))))

                result=driver.find_element(
                    By.CSS_SELECTOR, ".text-success.text-center").text
                if(len(result) == 0):
                    reply="Sorry, not alloted for the entered BOID."
                    print(reply)
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
                else:
                    reply=result
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
            elif("search image" in msg):
                imageSearch(self, msg)

            elif("program to" in msg):
                programming_solution(self, msg)
            elif("translate" in msg):
                reply=translator(self, msg, msg.split()[-1])
                print(reply)
                sendQuery()
            elif "weather of" in msg:
                indx=msg.index("weather of")
                query=msg[indx+11:]
                reply=weather(query)
                sendQuery()
            elif "corona of" in msg:
                corona_details(msg.split()[2])
            elif ("calculus" in msg):
                stepWiseCalculus(" ".join(msg.split(" ")[1:]))
            elif ("algebra" in msg):
                stepWiseAlgebra(" ".join(msg.split(" ")[1:]))
            elif ("query" in msg):
                stepWiseQueries(" ".join(msg.split(" ")[1:]))

            elif "find" in msg or "solve" in msg or "evaluate" in msg or "calculate" in msg or "value" in msg or "convert" in msg or "simplify" in msg or "generate" in msg:
                app_id="Y98QH3-24PWX83VGA"
                client=wolframalpha.Client(app_id)
                query=msg.split()[1:]
                res=client.query(' '.join(query))
                answer=next(res.results).text
                reply=f'Answer: {answer.replace("sqrt", "√")}'
                sendQuery()

            elif ("search user" in msg or "search friend" in msg):
                searchForUsers(self)

            elif("mute conversation" in msg):
                try:
                    self.muteThread(mute_time=-1, thread_id=author_id)
                    reply="muted 🔕"
                    sendQuery()
                except:
                    pass
            elif ("busy" in msg):
                reply="Nobody is busy. Only things are prioritized."
                sendMsg()
            elif("help" in msg):
                reply="Sure! What should I do?"
                sendMsg()
            elif("clever" in msg):
                reply="Yes, i am clever. hope you will be clever soon."
                sendMsg()
            elif("crazy" in msg):
                reply="Anything wrong about that."
                sendMsg()
            elif ("are funny" in msg):
                reply="No. I am not. You are."
                sendMsg()
            elif ("marry me" in msg):
                reply="Yes, if you are nice and kind girl. But if you are boy RIP."
                sendMsg()
            elif ("you from" in msg):
                reply="I am from Nepal. Currently living in Kathmandu"
                sendMsg()
            elif ("you sure" in msg):
                reply="Yes. I'm sure."
                sendMsg()
            elif ("great" in msg):
                reply="Thanks!"
                sendMsg()
            elif ("no problem" in msg):
                reply="Okay😊🙂"
                sendMsg()
            elif ("thank you" in msg):
                reply="You're welcome😊🙂"
                sendMsg()
            elif ("thanks" in msg):
                reply="You're welcome🙂"
                sendMsg()
            elif ("well done" in msg):
                reply="Thanks🙂"
                sendMsg()
            elif ("wow" in msg):
                reply="🙂😊"
                sendMsg()
            elif ("wow" in msg):
                reply="🙂😊"
                sendMsg()
            elif ("bye" in msg):
                reply="bye👋"
                sendMsg()
            elif ("good morning" in msg):
                reply="Good Morning🌅🌺"
                sendMsg()
            elif ("goodnight" in msg):
                reply="good night🌃🌙"
                sendMsg()
            elif ("good night" in msg or msg == "gn"):
                reply="good night🌃🌙"
                sendMsg()
            elif ("hello" in msg):
                reply="Hi"
                sendMsg()
            elif ("hello" in msg or "hlo" in msg):
                reply="Hi"
                sendMsg()
            elif (msg == "hi"):
                reply="Hello! How can I help you?"
                sendMsg()
            

        except:
            pass


        self.markAsDelivered(author_id, thread_id)

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        if(author_id == self.uid):
            pass
        else:
            try:
                conn=sqlite3.connect("messages.db")
                c=conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg=c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg=fetched_msg[0][1]
                if("//scontent.xx.fbc" in unsent_msg):
                    reply=f"You just unsent an image"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    reply=f"You just unsent a message:\n{unsent_msg} "
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
            except:
                pass

    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You changed the theme ✌️😎"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onEmojiChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You changed the emoji 😎. Great!"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onImageChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="This image looks nice. 💕🔥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onNicknameChange(self, mid=None, author_id=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply=f"You just changed the nickname to {new_nickname} But why? 😁🤔😶"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onReactionRemoved(self, mid=None, author_id=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You just removed reaction from the message."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply="You just started a call 📞🎥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallEnded(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply="Bye 👋🙋‍♂️"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onUserJoinedCall(mid=None, joined_id=None, is_video_call=None,
                         thread_id=None, thread_type=None, **kwargs):
        reply=f"New user with user_id {joined_id} has joined a call"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)


cookies = {"sb": "ILAxYj1fpwqBiFH9ALOFfnK3", "datr": "ILAxYrcEiavR7q2NIam4bu2T", "dpr": "1.25", "wd": "1536x746", "c_user": "100057654608526", "xs": "26%3A2KfeEByD4leReA%3A2%3A1647427509%3A-1%3A3707%3A%3AAcXCMMeQpIMvIQW8i9_0DuOlclNRqscJ4nplNxBRJA", "fr": "0U9mYOr3VwhZ5aJcd.AWUJspSLXucXGfmrmvtsqKfH0mA.BiMbAg.Ch.AAA.0.0.BiMb-4.AWUDuQo7Mvg", "presence": "C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1647427545293%2C%22v%22%3A1%7D"}

# enter your email and password facebook
client=ChatBot("",
                "", session_cookies=cookies)
print(client.isLoggedIn())

try:
    client.listen()
except:
    time.sleep(3)
    client.listen()
