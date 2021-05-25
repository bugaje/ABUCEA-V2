import picamera  
from gtts import gTTS
import os

import argparse
#import urllib2
import base64
import json
from subprocess import call
import time
import datetime
import wikipedia

import speech_recognition as sr
import re
import webbrowser
import smtplib
import requests
#from weather import Weather

#-*- coding: utf-8 -*-

import smbus
import time

#New Modules
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib3
import json
from bs4 import BeautifulSoup as soup
#import urllib.request as urlopen
import wikipedia
import random
#import request
from time import strftime
#import urllib.request  as urllib2
#import urlopen
from subprocess import call
import RPi.GPIO as GPIO2 # Import Raspberry Pi GPIO library
GPIO2.setwarnings(False) # Ignore warning for now
GPIO2.setmode(GPIO2.BCM) # Use physical pin numbering
GPIO2.setup(10, GPIO2.IN, pull_up_down=GPIO2.PUD_DOWN)# 
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
import random
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BCM)# Use physical pin numbering
RGB1_R = 2
RGB1_G = 3
RGB1_B = 4
RGB2_R = 17
RGB2_G = 27
RGB2_B = 22
k = list([RGB1_R, RGB1_G,RGB1_B, RGB2_R, RGB2_G, RGB2_B])
randomcolors  = [(0,0,1),(0,1,0), (0,1,1), (1,0,1), (1,1,0),(1,1,1),
                 (1,0,0)]
for p in k:
    GPIO.setup(p, GPIO.OUT, initial=GPIO.LOW)
    


options = {"your google credential keys goes here pub/sub generated google cloud platform"} //API KEY GENERATED FROM GOOGLE CLOUD PLATFORM


from google.cloud import vision
client = vision.ImageAnnotatorClient(options)

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


a = 'I have looked at the environment, I will now analyze' 
x = 'I  Can see  '

address = 0x04
bus = smbus.SMBus(1)

def sound(inp):
    #   -ven+m7:    Male voice
    #  The variants are +m1 +m2 +m3 +m4 +m5 +m6 +m7 for male voices and +f1 +f2 +f3 +f4 which simulate female voices by using higher pitches. Other variants include +croak and +whisper.
    #  Run the command espeak --voices for a list of voices.
    #   -s180:      set reading to 180 Words per minute
    #   -k20:       Emphasis on Capital letters
        randcolor = random.randint(0,6)

        tts = gTTS(text = inp, lang = 'en-us')
        tts.save("done.mp3")
        gotten = randomcolors[randcolor]
        print("first value",gotten, gotten[0], gotten[1])
        GPIO.output(RGB1_R, gotten[0])
        GPIO.output(RGB1_G, gotten[1])
        GPIO.output(RGB1_B, gotten[2])
        GPIO.output(RGB2_R, gotten[0])
        GPIO.output(RGB2_G, gotten[1])
        GPIO.output(RGB2_B, gotten[2])
        os.system("mpg321 done.mp3")
        
def myCommand():
    "listens for commands"
    GPIO.output(RGB1_R, 0)
    GPIO.output(RGB1_G, 0)
    GPIO.output(RGB1_B, 0)
    GPIO.output(RGB2_R, 0)
    GPIO.output(RGB2_G, 0)
    GPIO.output(RGB2_B, 0)
    os.system('sudo ./hub-ctrl -h 0 -P 2 -p 0')
    r = sr.Recognizer()
    i = 0
    devindex = 0
    for k in sr.Microphone.list_microphone_names():
        if k.startswith('USB'):
            devindex = i
            break
        i = i+1
    os.system('sudo ./hub-ctrl -h 0 -P 2 -p 0 ; sleep 5; sudo ./hub-ctrl -h 0 -P 2 -p 1; ')
    with sr.Microphone(device_index=devindex) as source:
        print('Ready...')
        sound('Waitiing for voice command.')
        #r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        #os.system('sudo ./hub-ctrl -h 0 -P 2 -p 0 ; sleep 5; sudo ./hub-ctrl -h 0 -P 2 -p 1; ')

    try:
        print("converting to text.........")
        command = r.recognize_google(audio, language = 'en-NG').lower()
        print('You said: ' + command + '\n')
        

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last voice command could not be heard')
        sound('Your voice command could not be heard. please say it again!')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"

    if 'open google' in command:
        reg_ex = re.search('open google (.*)', command)
        url = 'https://www.google.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sound('Done! i have opened google.com')

    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sound('Done!')
        else:
            pass
    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https:/www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sound('The Reddit content has been opened for you Sir.')
        sys.exit()
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            sound(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sound('The website you have requested has been opened for you Sir.')
        else:
            pass
    elif 'hello' in command or 'hey assistant' in command or 'hay' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sound('Hello Sir. Good morning! I am ABUCEA personal assistant, how may i help you.')
        elif 12 <= day_time < 18:
            sound('Hello Sir. Good afternoon! I am ABUCEA personal assistant, how may i help you.')
        else:
            sound('Hello Sir. Good evening! I am ABUCEA personal assistant, how may i help you.')
    elif 'news for today' in command or 'latest news' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:5]:
                sound(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)
    elif 'current weather' in command or 'current temperature' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sound('The current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
    
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                alltext  = ny.content
                print(type(alltext))
                sound(alltext[:500])
        except Exception as e:
               #print(e)
                sound(e)
    elif 'what is the meaning' in command:
        reg_ex = re.search('what is the meaning (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                alltext  = ny.content
                print(type(alltext))
                sound(alltext[:500])
        except Exception as e:
        # print(e)
                sound(e)
    elif 'history of' in command:
        reg_ex = re.search('history of (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                alltext = ny.content
                sound(alltext[:500])
        except Exception as e:
                sound(e)
        
    elif 'what are you doing' in command:
        sound('Just doing my thing...do you want me to do something for you sir..')
    elif 'tell me a joke' in command or 'make me laugh' in command or 'tell me joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            sound(str(res.json()['joke']))
        else:
            sound('oops!I ran out of jokes today')
            
    elif 'history of ahmadu bello university' in command or 'something about a b u zaria' in command or 'history of a b u zaria' in command:
        sound('''Ahmadu Bello University ABU is a federal government research university located in Zaria, Kaduna State. ABU was founded on October 4, 1962,
              as the University of Northern Nigeria.The university operates three main campuses: Samaru and Kongo in Zaria, and School of Basic Studies in Funtua.
              The Samaru campus houses the administrative offices, sciences, social-sciences, arts and languages, education,environmental design, engineering
              medical sciences agricultural sciences and research facilities. The Kongo campus hosts the Faculties of Law and Administration.
              The Faculty of Administration consists of Accounting, Business Administration, Local Government and Development Studies and Public Administration Departments.
              Additionally, the university is responsible for a variety of other institutions and programs at other locations.
              The university is named after the Sardauna of Sokoto, Alhaji Sir Ahmadu Bello, the first premier of Northern Nigeria.The university runs a wide variety of undergraduate and graduate programs (and offers associate degrees and vocational and remedial programs. The university has a large medical program with its own A.B.U. Teaching Hospital, one of the largest teaching hospitals in Nigeria and Africa.''')
    elif 'first chancellor of ahmadu bello university' in command or 'first ABU chancellor in 1962' in command or 'first a b u chancellor' in command:
        sound('''Alhaji Sir Ahmadu Bello KBE June 12, 1910 to January 15, 1966 was a Nigerian politician who was the first and only premier of the Northern Nigeria region.
              He also held the title of the Sardauna of Sokoto. Bello and Abubakar Tafawa Balewa were major figures in Northern Nigeria pre independence politics and both
              men played major roles in negotiations about the region's place in an independent Nigeria. As leader of the Northern People's Congress, he was a dominant
              personality in Nigerian politics throughout the early Nigerian Federation and the First Nigerian Republic.''')
    elif 'second chancellor of ahmadu bello university' in command or 'second A B U chancellor' in command or 'second chancellor' in command:
        sound("Omo n Oba n Edo Uku Akpolokpolo, Akenzua two January 7, 1899 to June 11, 1978 was the Oba of Benin traditional leader of the Edo people, in Nigeria from 1933 until his death in 1978.")
    elif 'third ahmadu bello university chancellor' in command:
        sound('''Sir Egbert Udo Udoma 21 June 1917 to 2 February 1998 was a lawyer and justice of the Nigerian Supreme Court. He was Chief Justice of Uganda from 1963 to 1969.
              He spent 13 years as a judge on the Supreme Court of Nigeria and was chairman of the Constituent Assembly from 1977 to 1978. He was one of the founding fathers of Nigeria.
              Udoma was one of the first black Africans to earn a PhD in Law in 1944 from Oxford University. He was a devoted Methodist and a holder of Knight of John Wesley (KJW).''')
    elif 'fourth ahmadu bello university chancellor' in command:
        sound('''Chief Obafemi Jeremiah Oyeniyi Awolowo, GCFR Yoruba: obafemi Awolowo, 6 March 1909 to 9 May 1987, was a Nigerian nationalist and statesman who played a key role in Nigeria's independence movement
              the First and Second Republics and the Civil War. The son of a Yoruba farmer, he was one of the truly self-made men among his contemporaries in Nigeria.''')
    elif 'fifth ahmadu bello university chancellor' in command:
        sound('''Muhammadu Barkindo Aliyu Musdafa born February 1944 was turbaned on 18 March 2010 as the traditional ruler, title Lamido of Adamawa in Adamawa State Northeastern Nigeria. ",
              The ceremony followed by the approval of the state governor Murtala Nyako.''')
    elif '6th ahmadu bello university chancellor' in command:
        sound('''Sultan Muhammadu Sa'ad Abubakar born August 24, 1956 in Sokoto is the 20th Sultan of Sokoto, the titular ruler of Sokoto in northern Nigeria, head of Jama'atu Nasril Islam Society for the Support of Islam JNI
              and president-general of the Nigeria Supreme Council for Islamic Affairs NSCIA. As Sultan of Sokoto, he is considered the spiritual leader of Nigeria's fifty nine million Muslims, roughly twenty-seven percent
              of the nation's population.Sa'adu Abubakar succeeded his brother, Muhammadu Maccido, who died on ADC Airlines Flight 53, the flight crashed shortly after takeoff from Nnamdi Azikiwe International Airport
              and had been destined for Sokoto.''')
    elif 'current ahmadu bello university chancellor' in command or 'present chancellor' in command or 'chancellor of a b u' in command:
        sound('''Nnaemeka Alfred Achebe CFR, mni born 14 May 1941 is a royal and the 21st Obi of Onitsha, in Anambra State, South-Eastern Nigeria.He is chancellor of Ahmadu Bello University since 2015
              and was earlier chancellor of Kogi State University. Achebe also serves as the chairman of the board of Directors of Unilever Nigeria, and the Chairman of International Breweries ABInBev Nigeria.
              Before emerging as the Obi of Onitsha, in 2002, he had a long and distinguished career in the Royal Dutch Shell Group serving as Director in various companies in the group.''')
    elif 'vice chancellor of ahmadu bello university in 1961' in command or 'first vice chancellor' in command:
        sound('''Professor Norman Stanley Alexander Kt CBE 7 October 1907 to 26 March 1997 was a New Zealand physicist instrumental in the establishment of many Commonwealth universities
              including Ahmadu Bello University in Nigeria, and the Universities of the West Indies, the South Pacific and Botswana, Lesotho and Swaziland.''')
    elif 'vice chancellor of ahmadu bello university in 1966-1975' in command:
        sound("Professor Ishaya Sha'aibu Audu March 1, 1927 to August 29, 2005 was a Nigerian doctor, professor, and politician. A Hausa Christian, he served as Minister of External Affairs Foreign Minister from 1979 to 1983 under Shehu Shagari.")
    elif 'vice chancellor of ahmadu bello university in 1975-1978' in command:
        sound("Professor Iya Abubakar born 14 December 1934 is a Nigerian politician and mathematician who held multiple cabinet level appointments Minister of Defence and Minister of Internal Affairs during the Nigerian Second Republic and Senator for Adamawa North from May 1999 to May 2007.")
    elif 'vice chancellor of ahmadu bello university in 1978-1979' in command:
        sound("Professor Oladipo Akikugbe, he is a medical doctor.")
    elif 'vice chancellor of ahmadu bello university in 1979-1986' in command:
        sound("Professor Ango Abdullahi, is the leader of the Northern Elders' Forum NEF.")
    elif 'vice chancellor of ahmadu bello university in 1986-1991' in command:
        sound("Professor Adamu N. Muhammad, he is an entomologist.")
    elif 'vice chancellor of ahmadu bello university in 1991-1995' in command:
        sound("Professor Daniel Soror, he is veterinarian.")
    elif 'vice chancellor of ahmadu bello university in 1995-1998' in command:
        sound("Major General (retired) Mamman Kontagora (April 20, 1944 - May 29, 2013) was Military Administrator of the Federal Capital Territory, Nigeria during the transitional regime of General Abdulsalam Abubakar, handing over control to a civilian in May 1999.")
    elif 'vice chancellor of ahmadu bello university in 1999-2004' in command:
        sound("Professor Abdullahi Mahadi, he is historian.")
    elif 'vice chancellor of ahmadu bello university in 2004-2009' in command:
        sound("Professor Shehu Usman Abdullahi, he is veternarian.")
    elif 'vice chancellor of ahmadu bello university in 2009-2009' in command:
        sound("Professor Jarlath Udoudo Umoh is a professor of Veterinary medicine at Ahmadu Bello University. He is a fellow of the Nigerian Academy of Science, elected into the Academy's Fellowship at its Annual General Meeting held in January 2015.")
    elif 'vice chancellor of ahmadu bello university in 2009-2010' in command:
        sound("Professor Aliyu Mohammed, he is a linguist (English Language).")
    elif 'vice chancellor of ahmadu bello university in 2010-2015' in command:
        sound("Professor Abdullahi Mustapha (born 1 February 1948) is a Nigerian Professor of Medicinal Chemistry and former Vice Chancellor of Ahmadu Bello University, Zaria. He was succeeded by Professor Ibrahim Garba, the incumbent VC of the University.")
    elif 'vice chancellor of ahmadu bello university in 2015' in command or 'present vice chancellor' in command or 'vice chancellor' in command:
        sound("Professor Ibrahim Garba is a Nigerian geologist and university administrator. He is the current Vice Chancellor of Ahmadu Bello University, Zaria.He previously served as the Vice Chancellor of the Kano State University of Science and Technology, Wudil.")
    elif 'deputy vice chancellor admin of ahmadu bello university' in command:
        sound("Professor. Sadiq Zubair Abubakar.")
    elif 'deputy vice chancellor academic of ahmadu bello university' in command:
        sound("Professor. Danladi Amodu Ameh.")
    elif 'ahmadu bello university registrar' in command:
        sound("Mallam. Abdullahi Ahmad Kundila")
    elif 'ahmadu bello university bursar' in command:
        sound("Mallam. Yahaya Alhaji Hassan")
    elif 'ahmadu bello university librarian' in command:
        sound("Professor. Umar Ibrahim")
    elif 'Directorate of Academic Planning and Monitoring of ahmadu bello university' in command:
        sound("Professor Abba Ali Tijjani, from Department of Mathematic")
    elif 'director Institute of Education ahmadu bello university' in command:
        sound("Professor Muhammad Lawal Amin, Department of African Languages and Cultures.")
    elif 'Provost College of Medical Sciences ahmadu bello university' in command:
        sound("Professor Abdullahi J. Randawa, College of Medical Sciences.")
    elif 'deen Faculty of Basic Clinical Sciences ahmadu bello university' in command:
        sound("Professor Haruna I. Mukhtar, Department of Haematology and Blood Transfusion.")
    elif 'director University Advancement ahmadu bello university' in command:
        sound("Professor Mohammed K. Aliyu, Department of Archaeology.")
    elif 'director National Animal Production Research Institute ahmadu bello university' in command:
        sound("Professor Abdullahi Mohammed Kolo, National Animal Production Research Institute.")
    elif 'director Institute for Agricultural Research ahmadu bello university' in command:
        sound("Professor Mohammad Faguji Ishiyaku, Department of Plant Science.")
    elif 'director Distance Learning Centre ahmadu bello university' in command:
        sound("Dr. Aminu Ladan Sharehu, Department of Public Administration.")
    elif 'director Centre for Disaster Risk ahmadu bello university' in command:
        sound("Dr. Usman Ado Kibon, Department of Geography.")
    elif 'director ABU Hotels ahmadu bello university' in command:
        sound("Dr. Ahmad Bello, department of accounting.")
    elif 'director Centre for Energy Research ahmadu bello university' in command:
        sound("Professor Ita O. Bassey Ewa, Centre for Energy Research and Training.")
    elif 'director institute of computing and ict' in command:
        sound("Professor Muhammad Bashir Muazu, department of computer enginerring.")
    elif 'history of computer engineering department' in command or 'computer engineering department' in command:
        sound('''he Department, which became full fledged in November 2017, after several years of being part of the Department of Electrical and Computer Engineering, has functional, vibrant contemporary programs leading to the award of B.Eng, PGD, M.Sc and Ph.D in Computer Engineering
              and M.Sc and Ph.D in Control Engineering and the proposed Masters in IT and Systems (MITS). It is worth noting that the Department has the following broad research areas
              1. AI, Robotics and Control Systems Group. 2. Embedded Systems and Applications Development Group. 3. Networks and Security Group 4. Image Processing and Computer Vision Group
              Our long-term vision is that of becoming a regional center of excellence for imparting high level ICT and Control Engineering knowledge in order to develop skilled and globally competitive professionals to serve the needs of our nation and humanity in general''')
    
    
    elif 'who is the dean faculty of engineering' in command or 'who is din faculty of engineering' in command or 'present dean faculty of engineering' in command:
        sound('Professor Isma"l from water resourses engineering')
    elif 'a b u glance' in command or 'area of ABU zaria' in command or 'ABU locate' in command:
        sound('The Main Campus of Ahmadu Bello University is located in Samaru, a suburb of Zaria in Kaduna State, Nigeria. Samaru is situated on latitude 112o 12" N and longitude 07o 37" E, at an altitude of 550-700 meters. It is about 13km from Zaria-city on the Sokoto road, 8km to Shika and 7km from Bassawa')
    elif 'how many campus' in command or 'number of campusis in ABU zaria' in command:
        sound('The university operates two campuses: Samaru (main) and Kongo in Zaria. There is pre-degree school in Funtua a few kilometres from main campus owned by the university. The Samaru campus houses the administrative offices and the faculties of physical sciences, life sciences, social sciences, arts and languages, education, environmental design, engineering, medical sciences, agricultural sciences and research facilities. The Kongo campus hosts the faculties of Law and Administration. The Faculty of Administration consists of Accounting, Business Administration, Local Government and Development Studies and Public Administration Departments. Additionally, the university is responsible for other institutions and programmes at other locations')     
    elif 'number of faculties in A B U' in command or 'faculties' in command or 'departments' in command:
        sound('ABU Zaria currently has eighty-two (82) Academic Departments (or courses as some prefer to call it), twelve (12) Faculties, and twelve (12) Research Institutes and Specialized Centres.')      
    elif 'who is the father' in command or 'who is the founder of ABU zaria' in command:
        sound('Sir. Ahmadu Bello Sardauna of sokoto')
    elif 'what is your name' in command or 'what is your personal name' in command or 'tell me about yourself' in command or 'tell me something about yourself' in command:
        sound('My name is Zazzau officially called ABU SEER,the zazzau version two, am the first cloud based AI personal assistant robot in A B U, Zaria.')
    elif 'how old are you' in command or 'what is your age' in command:
        sound('I was created on fourth of October, 2019') 
    elif 'who is the head of computer department' in command or 'who is HOD of computer engineering' in command: 
        sound('Professor Muhammad Bashir Muazu')
    elif 'VC of ABU Zaria' in command or 'chancellor of A B U Zaria' in command: 
        sound('Professor Ibrahim Garba')
    elif 'time' in command or 'date' in command:
        sound('Today\'s date is...')
        sound(str(datetime.datetime.now()))

    elif 'emotion' in command or 'feeling' in command or 'mood' in command:
            sound('Look at the camera am going to snap you now, to see how you are feeling.')
            takephoto() # First take a picture
            """Run a label request on a single image"""

            with open('image.jpg', 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.logo_detection(image=image)


            response = client.label_detection(image=image)
            labels = response.label_annotations
            print('Labels:')
            take_emotion()
        #detect_faces('faces.png')
    elif 'what can you see' in command:
            sound('Let me look around and check')
            takephoto() 
            with open('image.jpg', 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.logo_detection(image=image)


            response = client.label_detection(image=image)
            labels = response.label_annotations
            print('Labels:')
            i = 0 
            for label in labels:
                if (i < 4):
                    print(label.description)
                    sound(x+label.description)
                    i += 1
                else:
                    break
    elif 'who is the governor of Abia state' in command or 'governor of Abia' in command:
        sound("Okezie Victor Ikpeazu is the ninth and current Governor of Abia State, in office since May 29, 2015. He was elected on the platform of the Peoples Democratic Party.He was re-elected as the governor of Abia state after winning the March 9th, gubernatorial election")
    elif 'who is the current governor of Adamawa state' in command or 'governor adamawa' in command:
        sound('''Ahmadu Umaru Fintiri is the current governor of Adamawa State. He was a member of the Adamawa State House of Assembly, and was appointed the Speaker of the House. He became the acting Governor of Adamawa State Nigeria, following the impeachment of admiral Murtala Nyako in July 2014,handing later to Bala James Ngilari after serving for three months.
              Fintiri won the governorship election of Adamawa State that took place on the 9th of March 2019, however, the election was declared inconclusive because the number of cancelled votes was more than the margin between the winner and his close opponent. Umaru Fintiri was declared winner of the election in the early hours of Friday after having secured 376,552
              votes to defeat incumbent Governor Jibrilla Bindow of the All Progressives Congress (APC) who polled 336,386 votes.''')
    elif 'who is the governor of Akwa Ibom state' in command or 'governor akwa ibom' in command:
        sound("Udom Gabriel Emmanuel (born 11 July 1966) is the governor of Akwa Ibom State of Nigeria, in office since 29 May 2015. He ran successfully for the office of governor in the April 2015 elections on the platform of Akwa Ibom State People's Democratic Party. He was re-elected as the governor of Akwa Ibom State on the 29th of May, 2019")
    elif 'who is the current governor of Anambra state' in command or 'governor anambra' in command:
        sound("Chief Willie Obiano (born August 8, 1955) is a Nigerian banker, technocrat, politician and the fourth Democratic Governor of Anambra State")
    elif 'who is the governor of bauchi state' in command or 'governor bauchi' in command:
        sound('''Bala Abdulkadir Mohammed (born 5 October 1958) was elected Senator for Bauchi South, in Bauchi State, Nigeria in April 2007. He was appointed Minister of FCT (Federal Capital Territory) on 8 April 2010, when Acting President Goodluck Jonathan announced his new cabinet.He is the Governor-elect of Bauchi State in 2019,
              suplimentary governorship election under the platform of People's Democratic Party PDP.''')
    elif 'who is the governor of bayelsa state' in command or 'governor bayelsa' in command:
        sound("Seriake Henry Dickson (born 28 January 1966) is a Nigerian politician. He assumed his role as the Governor of Bayelsa State in southern Nigeria on 14 February 2012. He was a member of the House of Representatives from 2007 until 2012")
    elif 'who is the current governor of benue state' in command or 'governor of benue state' in command or 'present governor of benue state' in command:
        sound("Samuel Ioraer Ortom is a Nigerian philanthropist, businessman, politician and administrator. He was a Minister of State Trade and Investments in Nigeria during the presidency of Goodluck Jonathan. Ortom was elected governor of Benue State as a member of the All Progressives Congress in 2015. He was re-elected as governors on 29 May 2019")
    elif 'who is the governor of borno state' in command or 'governor of borno state' in command or 'present governor of borno state' in command:
        sound("Babagana Umara Zulum (born August 26, 1969) is a Nigerian professor and politician. He was elected has the governor of Borno State in the governorship election of March 9, 2019 under the platform of the All Progressive Congress (APC).He was sworn in has governor of Borno State on May 29, 2019")
    elif 'who is the governor of cross river state' in command or 'governor of river state' in command or 'present governor of river state' in command:
        sound('''Benedict Bengioushuye Ayade, (born on 2 March 1968), is a Nigerian politician and the current Governor of Cross River State since 29 May 2015. He ran successfully for the office of Governor in April 2015 on the platform of People's Democratic Party (PDP). Before that, he was a member of the 7th Senate of Nigeria.
              He was re-elected as the governor of Cross River State in the 2019 gubernatorial elections.''')
    elif 'who is the governor of delta state' in command or 'governor of delta state' in command or 'present governor of delta state' in command:
        sound('''Ifeanyi Arthur Okowa (born 8 July 1959) is a Nigerian politician who is the incumbent Governor of Delta State. He was inaugurated as a governor on 29 May 2015 after winning the state elections conducted in April 2015. Before his governorship, he was elected senator for Delta North, in Delta State,
              Nigeria, in the April 2011 national elections. He ran on the People's Democratic Party (PDP) platform. He is an Ika from Owa-Alero in Delta State, Nigeria. He is also the first person from Anioma to clinch the governorship position of Delta State. He was re-elected as the governor of Delta State on May 29, 2019.''')
    elif 'who is the governor of ebonyi state' in command or 'governor of ebonyi state' in command or 'present governor of ebonyi state' in command:
        sound("David Nweze Umahi (known popularly as Dave Umahi, born January 1, 1964) is a Nigerian politician who is serving as the current Governor of Ebonyi State, Nigeria")
    elif 'who is the governor of edo state' in command or 'governor of edo state' in command or 'present governor of edo state' in command:
        sound('''Godwin Nogheghase Obaseki (born 1 July, 1957 in Benin City, Nigeria) is a Nigerian businessman and politician, who is currently serving as the Executive Governor of Edo State. He was sworn in as the governor on 12 November 2016.
              He was the Chairman of the Edo State Economic and Strategy Team inaugurated by former Governor Adams Oshiomole in March 2009.''')
    elif 'who is the governor of ekiti state' in command or 'governor of ekiti state' in command or 'present governor of ekiti state' in command:
        sound('''John Olukayode Fayemi, (born 9 February 1965) is the Governor of Ekiti State and a native of Isan-Ekiti in Oye Local Government of Ekiti State, Nigeria. He previously held the office of the Governor of Ekiti State between 2010 and 2014. He resigned as the Minister of Solid Minerals Development on 30 May 2018",
              to contest for the Ekiti State governorship election for the second time, an election perceived to be a battle between himself and his political rival, Fayose.''')
    elif 'who is the governor of enugu state' in command or 'governor of enugu state' in command or 'present governor of enugu state' in command:
        sound('''Lawrence Ifeanyi Ugwuanyi (popularly known as 'Gburugburu') is a Nigerian politician who was elected as the Executive Governor of Enugu State in April 2015 and was sworn in on 29 May, 2015.He was a member of the House of Representatives of the Federal Republic of Nigeria for 12 years.
              self published source He is a People's Democratic Party (PDP) member and represented Igboeze North/Udenu Federal Constinuency of Enugu State. Ugwuanyi was elected the Governor of Enugu State under the PDP. He was re-elected as the governor of Enugu State on May 29, 2019.''')
    elif 'who is the governor of gombe state' in command or 'governor of gombe state' in command or 'present governor of gombe state' in command:
        sound("Muhammad Inuwa Yahaya (born October 9, 1961) is a Nigerian businessman and politician. He is the Executive Governor of Gombe State elected on 9 March 2019 under the platform of the All Progressive Congress (APC)")
    elif 'who is the governor of Imo state' in command or 'governor of imo state' in command or 'present governor of imo state' in command:
        sound('''Rt. Hon Chief Sir Emeka Ihedioha (born 24 March 1965) is a Nigerian politician and Businessman. He is the Governor of Imo State.He is a Peoples Democratic Party (PDP) member and represented the Aboh Mbaise Ngor Okpala Federal Constituency of Imo State.
              He was also the former deputy speaker of the House of Representatives of Nigeria. He is a Commander of the Order of the Niger and holds the title CON.''')
    elif 'who is the governor of jigawa state' in command or 'governor of jigawa state' in command or 'present governor of jigawa state' in command:
        sound("Mohammed Badaru Abubakar (born in Babura in 1962) is the 4th democratically elected Governor of Jigawa State in Nigeria. He is the Presidential Committee Chairman on Fertilizer and also the Presidential Committee Chairman on Non oil Revenue.")
    elif 'who is the governor of kaduna state' in command or 'governor of kaduna state' in command or 'present governor of kaduna state' in command:
        sound('''Malam Nasir Ahmad El-Rufai born 16 February 1960,is a Nigerian politician who is the Governor of Kaduna State, Nigeria. He was the former Director General of Bureau of Public Enterprises, the head of privatisation agency in Nigeria.
              He was the Minister of the Federal Capital Territory, Abuja from 16 July 2003 to 29 May 2007.He is a member of All Progressives Congress (APC) and was elected as the Executive Governor of Kaduna State during the 2015 general elections in Nigeria.''')
    elif 'who is the governor of kano state' in command or 'governor of kano state' in command or 'name of kano state governor' in command or 'present governor of kano state' in command:
        sound("Abdullahi Umar Ganduje, OFR (born 25 December 1945) is a Nigerian politician and current Governor of Kano State since 2015. He previously served as deputy governor twice between 1999 to 2003 and 2011 to 2015. In October 2018, he appeared in a viral video collecting bribe from a contractor in the state.")
    elif 'who is the governor of katsina state' in command or 'governor of katsina state' in command or 'name of katsina state governor' in command:
        sound("Aminu Bello Masari (born 29 May 1950) is a Nigerian politician and current Governor of Katsina State. He was the speaker of the Nigerian House of Representatives between 2003 and 2007. Masari hails from Katsina State.")
    elif 'who is the governor off kebbi state' in command or 'governor of kebbi state' in command or 'present governor of kebbi state' in command:
        sound('''Abubakar Atiku Bagudu (born 26 December 1961) is a Nigerian politician who was the Senator for Kebbi Central constituency of Kebbi state after contesting in a bye-election when Sen Adamu Aleru was appointed minister of the Federal capital territory.
              Atiku bagudu was in the red chamber from December 2009 to May 2015. He became the flag bearer of the political party All Progressives Congress (APC) gubernatorial candidate in Nigeria's 2015 general elections and was elected Governor
              He was re-elected governor of Kebbi state.''')
    elif 'who is the governor of kogi state' in command or 'governor of kogi state' in command or 'present governor of kogi state' in command:
        sound('''Yahya Adoza Bello (born June 18, 1975) is a Nigerian politician, businessman and the current Governor of Kogi State.Bello was declared winner of the 2015 Kogi gubernatorial election after he was chosen on the platform of the All Progressives Congress
              as the replacement for the late Abubakar Audu who originally won the election but died before the result was declared.''')
    elif 'who is the governor of kwara state' in command or 'governor of kwara state' in command or 'present governor of kwara state' in command:
        sound('''AbdulRahman AbdulRazaq the incumbent Governor of Kwara State (born 5 February 1960) is a Nigerian businessman and politician. He was the CEO of First Fuels Limited. He contested for the governor of Kwara State in 1999, 2003, 2007, 2011 and 2015 respectively
              under the Congress for Progressive Change political party but was successively defeated in 1999 by Mohammed Alabi Lawal, by Bukola Saraki in 2003 and 2007, and by Abdulfatah Ahmed in 2011 and 2015. However in 2019 he contested again under the ruling political party in Nigeria
              APC and emerged as the governor of Kwara State, after he successfully won the 2019 governorship election in the state.''')
    elif 'who is the governor of lagos state' in command or 'governor of lagos state' in command or 'present governor of lagos state' in command:
        sound('''Babajide Olusola Sanwo-Olu (born June 25, 1965) is a Nigerian Politician and the current Governor of Lagos State, he was announced the governor under the platform of the All Progressives Congress after contesting and unexpectedly winning the gubernatorial
              primaries under the All Progressives Congress against incumbent governor, Akinwunmi Ambode of Lagos State in October 2018.''')
    elif 'who is the governor of nasarawa state' in command or 'governor nasarawa' in command:
        sound("Engineer Abdullahi Sule (born December 26, 1959) is a Nigerian entrepreneur, businessman and politician. He is the Governor of Nasarawa State in the 2019 Governorship election under the platform of the All Progressive Congress (APC)")
    elif 'who is the governor of niger state' in command or 'governor of niger state' in command or 'present governor of niger state' in command:
        sound("Abubakar Sani Bello also known as Lolo; He is a Nigerian politician and is the current Governor of Niger State, Nigeria")
    elif 'who is the governor of ogun state' in command or 'governor of ogun state' in command or 'present governor of ogun state' in command:
        sound('''Dapo Abiodun (born 29 May 1960) is a Nigerian businessman and politician, who is the Governor of Ogun State after winning the 2019 general elections under the platform of the All Progressive Congress.
              Dapo Abiodun is the board Chairman of the Corporate Affairs Commission. He is the managing director of Heyden Petroleum and the founder of First Power Limited.On 10 March 2019
              he was declared Governor Elect of Ogun State by the Independent National Electoral Commission. He was sworn in as Governor of Ogun State on 29 May 2019.''')
    elif 'who is the governor of ondo state' in command or 'governor of ondo state' in command or 'present governor of ondo state' in command:
        sound('''Oluwarotimi Odunayo Akeredolu, SAN, or Rotimi Akeredolu, (born 21 July 1956) is a Nigerian politician and lawyer who is also the Governor of Ondo State,Nigeria and also a Senior Advocate of Nigeria (SAN)
              who became president of the Nigerian Bar Association in 2008.Akeredolu was also a Managing Partner at the Law Firm of Olujinmi & Akeredolu, a Law Firm he co-founded with Chief Akin Olujinmi,
              a former Attorney General and Minister for Justice in Nigeria.''')
    elif 'who is the governor of osun state' in command or 'governor of osun state' in command or 'present governor of osun state' in command:
        sound('''Adegboyega Oyetola (born September 29, 1954) is a Nigerian politician and Governor of Osun State. He contested the Osun State gubernatorial candidate on the platform of the All Progressives Congress (APC) for the September 22, 2018
              gubernatorial election and he won. On March 23, 2019 Tribunal declared him to have not been legally returned and orders INEC to issue certificates of return to Senator Adeleke of the PDP which is expected to be contested at the Court of Appeal
              Prior to his winning the election, he was the Chief of Staff to Rauf Aregbesola, his predecessor.''')
    elif 'who is the governor of oyo state' in command or 'governor of oyo state' in command or 'present governor of oyo state' in command:
        sound('''Oluseyi Abiodun Makinde (born 25 December 1967) is a Nigerian businessman, politician and philanthropist. He is the governor of Oyo State in South-western Nigeria. He is an engineer and a subject matter expert on fluid and gas metering.
              Until August 2018, he was the Group Managing Director of Makon Group Limited; an indigenous oil and gas company in Nigeria.''')
    elif 'who is the governor of plateau state' in command or 'governor of plateau state' in command or 'governor of jos' in command:
        sound("Simon Lalong (born 5 May 1963 in Shendam, Plateau State) is a Nigerian lawyer and politician, who is the present Governor of Plateau State, Nigeria")
    elif 'who is the governor of river state' in command or 'governor of river state' in command or 'present governor of rivers state' in command:
        sound('''Ezenwo Nyesom Wike CON (born 13 March 1963), also known variously as Ezebunwo Nyesom Wike, Nyesom Ezenwo Wike, Nyesom Ezebunwo Wike or Nyesom Wike is a Nigerian politician and lawyer who is the sixth and current Governor of Rivers State.
              He is an Ikwerre from Rumuepirikom in Obio-Akpor, Rivers State. He is a member of the People's Democratic Party and was educated at Rivers State University of Science and Technology.''')
    elif 'who is the governor of sokoto state' in command or 'governor of sokoto state' in command or 'present governor of sokoto state' in command:
        sound('''Aminu Waziri Tambuwal (born January 10, 1966) is currently the governor of Sokoto State. He initially became the governor of Sokoto state after his election during the 2015 General Elections into the office and was re-elected after the 2019 General Elections.
              Aminu Tambuwal is a member of the People's Democratic Party and served as the 10th Speaker of the House of Representatives of Nigeria, also representing the Tambuwal Kebbe Federal Constituency of Sokoto State as an honorable.''')
    elif 'who is the governor of taraba state' in command or 'governor of taraba state' in command or 'present governor of taraba state' in command:
        sound("Darius Dickson Ishaku, FNIA, FNITP (born 30 July 1954) is a Nigerian Architect, Urban planner, University lecturer and Political figure. He is a member of the People's Democratic Party and the Governor of Taraba State.")
    elif 'who is the governor of yobe state' in command or 'governor of yobe state' in command or 'present governor of yobe state' in command:
        sound('''Mai Mala Buni born November 11, 1967 in Buni Yadi, Yobe, Nigeria. is a Nigerian politician and the Governor of Yobe State, Nigeria.He was elected Governor during the 2019 Nigeria general elections under the platform All Progressives Congress APC party.Before being elected governor
              he was the Secretary General of the Nigeria's ruling party the All Progressives Congress.''')
    elif 'who is the governor of zamfara state' in command or 'governor of zamfara' in command or 'present governor of zamfara state' in command:
        sound("Bello Muhammad Matawalle (born in 1969) is the current Governor of Zamfara State, Nigeria. He contested under the platform of the Peoples Democratic Party (PDP).")
            
    elif 'who created you' in command or 'who create you' in command or 'who made you' in command or 'who is your maker' in command or 'who build you' in command:
        sound('I was created by ALIYU ISAH and BLESSED GUDA, the guys whom i never got to know them')
        
    elif 'move north' in command or 'move forward' in command or 'go forward' in command or 'go north' in command:
        sound('forward drive activated')
        writeNumber(int(ord('f')))
    elif 'move west' in command or 'move left' in command or 'go west' in command or 'go left' in command:
        sound('west drive activated')
        writeNumber(int(ord('w')))
    elif 'move east' in command or 'move right' in command:
        sound('east drive activated')
        writeNumber(int(ord('e')))
    elif 'move south' in command or 'move backward' in command or 'go backward' in command:
        sound('backward drive activated')
        writeNumber(int(ord('s')))
    elif 'stop' in command or 'halt' in command:
        sound('robot stopped')
        writeNumber(int(ord('h')))
    elif 'shutdown' in command or 'power off' in command or 'good bye' in command:
        sound("Power off")
        call(['shutdown', '-h', 'now'], shell=False)
            
    elif 'send email' in command:
        sound('Who is the recipient?')
        recipient = myCommand()
        if 'ali' in recipient:
            sound('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('aliyuisahprof@gmail.com', '64720609')

            #send message
            mail.sendmail('Guda Blessed', 'gudablessed@gmail.com', content)

            #end mail connection
            mail.close()

            sound('Email sent successfully.')
            
                        #  HISTORY OF NIGERIA        
    
    elif 'who are nigerians' in command or 'who are the nigerian citizens' in command:
        sound('''Nigerians or the Nigerian people are citizens of Nigeria or people with ancestry from Nigeria. Nigeria is composed of various ethnic groups and cultures and the term Nigerian refers to a citizenship-based civic nationality.
              Nigerians derive from over 250 ethnic groups and languages.Though there are multiple ethnic groups in Nigeria, economic factors result in significant mobility of Nigerians of multiple ethnic and religious backgrounds to reside
              in territories in Nigeria that are outside their ethnic or religious background, resulting in the mixing of the various ethnic and religious groups, especially in Nigeria"s cities.
              The English language is the lingua franca of Nigerians. 51.6% of Nigerians are Muslims and about 46.9% are Christians''')
    elif 'history of nigeria' in command or 'brief history of nigeria' in command:
        sound('''The history of Nigeria has been crucially impacted by the Transatlantic Slave Trade, which started in Nigeria in the late 15th century.
                Islam reached Nigeria through the Borno Empire between and Hausa States around during the 11th century, while Christianity came to Nigeria in the 15th century through Augustinian and Capuchin monks from Portugal.
                Evidence of iron smelting has also been excavated at sites in the Nsukka region of southeast Nigeria in what is now Igboland: dating to 2,000 BC at the site of Lejja and to 750 BC and at the site of Opi.
                Abacha died in 1998 and a fourth republic was later established the following year, which ended three decades of intermittent military rule The Hausa Kingdoms were a collection of states started by the Hausa people, situated between the Niger River and Lake Chad
                According to the Bayajidda legend, the Hausa states were founded by the sons of Bayajidda, a prince whose origin differs by tradition, but official canon records him as the person who married the last Kabara of Daura and heralded the end of the matriarchal monarchs that had erstwhile ruled the Hausa people''')
    elif 'who is the president of nigeria' in command or 'who is the nigerian president' in command:
        sound('''The President of the Federal Republic of Nigeria is the head of state and head of government of the Federal Republic of Nigeria. The President of Nigeria is also the commander-in-chief of the Nigerian Armed Forces. The President is elected in national elections
              which take place every four years. The offices, powers, and titles of the Head of State and the Head of Government were officially merged into the office of the Presidency under the 1979 Constitution of Nigeria. The current President, Muhammadu Buhari took office on May 29, 2015 as the 15th President of the Federal Republic of Nigeria''')
            
    elif 'who is the current president of nigeria' in command or 'current nigerian president' in command or 'president of nigeria' in command:
        sound('The current President, General Muhammadu Buhari took office on May 29, 2015 as the 15th President of the Federal Republic of Nigeria.')
    elif 'prime minister of nigeria' in command or 'who is the prime minister of nigeria' in command or 'prime minister' in command:
        sound('On October 1, 1960, Nigeria gained independence from Britain. An all-Nigerian Executive Council was headed by a Prime Minister, Alhaji Sir Abubakar Tafawa Balewa.')
    elif 'nigeria president in 1960' in command or 'nigerian president in 1963' in command or 'nigerian leader in 1960 to 1963' in command:
        sound('''Balewa is the only leader in Nigerian history to have been bestowed with the title of Prime Minister. He played a very important role in the transitional period between colonial and indigenous rule of Nigeria. His legacy was created by cooperation between ethnic groups and mediation of other African conflicts.
              Today his face is pictured on the five Naira note. Balewa was murdered during the military coup of Nigeria in 1966. His death spurred bloody counter-coup protests, especially in the Northern part of the country''')
    elif 'president of nigeria in 1963 to 1966' in command or 'president of nigeria in 1963' in command or 'president of nigeria in 1965' in command:
        sound('''Nmandi Azikiwe was the first President of Nigeria after the country became a fully independent republic and Nigeria cut ties with Britain almost completely. Azikiwe is well known for promoting modern Nigerian and African nationalism. Educated in the United States, Azikiwe worked as a journalist in Baltimore
              and Philadelphia and was already well known as a public figure on his return to Nigeria in 1937. In 1960, he established the University of Nigeria. Azikiwe held many political positions within Nigeria, including representing the Queen as head of state from 1960-1963, but he is best remembered as the first President of the country.''')
    elif 'president of nigeria in 1966' in command:
        sound('''Major-General Johnson Aguiyi-Ironsi was a senior Nigerian officer in the military, and led the 1966 military coup against Azikiwe"s government. The coup started by Aguiyi-Ironsi and his army killing the highest rank politicians in the North and West of the country (including Balewa, the first Prime Minister).
              His power grab did not last long in Nigeria, he was only in power for 194 days (January of 1966 until June of 1966), before being murdered in a counter coup by unhappy members of the Nigerian armed forces.''')
    elif 'president of nigeria in 1966 to 1975' in command:
        sound('''General Yakubu Gowon seized power after the counter-coup against Aguiyi-Ironsi. Soon after he had grabbed power, Gowon implemented genocidal tactics against the Igbo people in the north, killing more than 50,000. In 1967 after tensions had reached a boiling point, the Nigerian Civil War broke out.
              This was was caused by Eastern Nigerians (namely the Igbo people) desiring to secede from Nigeria and form their own country. Over 100,000 soldiers and 1,000,000 civilians were killed in the war, known as the Biafran War. Leading the country during the early 1970's oil boom, Gowon endorsed modernization of Nigeria
              creating infrastructure (international airport, a stadium, and an arts theater to name a few) that still stand today.''')
    elif 'president of nigeria in 1975 to 1976' in command:
        sound('''General Murtala Mohammed. After the third army-led coup in Nigeria, Mohammed was put into power. Mohammed removed from power a number of former high-ranking politicians and officials in an effort to differentiate his government from that of Gowon. Many of these fired public servants were trialed for corruption
              During his brief stint in office, the Nigerian government took over all broadcasting and media, creating a monopoly of communications for the government. As with many Nigerian leaders, Mohammed was assassinated. In February of 1976, after a failed coup attempt, Mohammed's vehicle was ambushed on his way to his offices and he was murdered.''')
    elif 'president of nigeria in 1976 to 1979' in command:
        sound('''Major General Olusegun Obasanjo. Obasanjo did not actively participate in the 1975 military coup, although he supported the coup and General Mohammed at the time. Subsequently, Obasanjo was named as deputy in Mohammed's government and was also targeted for assassination but managed to escape.
              Obasanjo re established security in the capital as well as army rule. By the time Obasanjo was in power (after Mohammed's murder), a program to restore civilian rule of Nigeria had been established and Obasanjo continued this program, holding general elections in 1979 and helping to create the
              Nigerian Constitution. On the 1st of October, 1979, Obasanjo peacefully handed power over to a civilian ruler, Shehu Shigari, marking the first time this happened in African history. Obasanjo was later democratically elected as President of Nigeria, which will be discussed later in this article''')
    elif 'president of nigeria in 1979-1983' in command:
        sound('''President Shehu Shagari. Shagari served as Nigeria's second President. Before becoming President, Shigari was appointed Minister of Economic Affairs in 1970, and later as the Minister of Finance by General Gowon in an attempt to include civilians in the rule of Nigeria. While running for President in 1979
              the National Party of Nigeria's motto was 'One Nation, One Destiny', which reflects Nigerian ethnic diversity as well as the common goal of Nigerian success. After the booming oil prices cooled off in 1981, the Nigerian economy was in trouble. The deterioration of the Nigerian economy, as well as consistent allegations of corruption and mismanagement
              led to Shigari being overthrown in yet another military coup in 1983.''')
    elif 'president of nigeria in 1983-1985' in command:
        sound('''Major-General Muhammadu Buhari. After successfully overthrowing the democratically elected government of Shagari, Buhari justified the Army's actions in 1983 by defining the civilian government as having been corrupt and hopeless. Buhari was quick to indefinitely suspend Nigeria's 1979 constitution. The harsh reality of how bad the Nigerian economy
              was during this time prompted Buhari to quickly implement policies that would encourage economic stability. These policies included the raising of interest rates, major cut back to public and government spending, and prohibiting the government from borrowing more money. Buhari also cut Nigeria's ties with the International Monetary Fund during this period.
              Buhari's tenure is known for the harsh policies the government implemented to protect itself, with many Nigerians, who were seen as a security threat by the government, being detained, jailed, and even executed during his rule''')
    elif 'president of nigeria in 1985-1993' in command:
        sound('''General Ibrahim Babangida. Nigerians, in particular the Army leadership, were becoming unhappy with Buhari's harsh methods of keeping corruption and poor discipline to a minimum. This led to an uncharacteristically bloodless coup whose leaders promised to end the constant human rights abuses by the previous regime.
              Babangida took power with support of loyal mid level military personnel which he had strategically placed into positions to benefit his aspirations of power. In 1990, Babangida's government was almost overthrown by a failed coup attempt from the Army. In June of 1993, Presidential elections were held in Nigeria with
              the goal of civilian rule being restored. After these elections, Babangida and his government decided to nullify the results, which led to civil unrest and labor strikes in the country. Many Nigerians believe this government was the most corrupt in Nigerian history.''')
    elif 'president of nigeria in 1993' in command:
        sound('''President Ernest Shonekan. After the civil and economic unrest of 1993, Babangida caved to public pressure and appointed Shonekan as the interim President of the country in August of 1993. By this point in time, inflation in Nigeria had become uncontrollable, and foreign investments in non-oil related industries
              had significantly waned. During his brief time as President, Shonekan tried to create a timetable that would lead the Nigerian people back to a democratic rule. This initiative failed as Shonekan's interim administration only lasted three months until he was overthrown by his own Secretary of Defence, Sani Abacha.
              Interestingly, many democratic supporters saw Shonekan as an obstacle to Nigerian prosperity and growth, as well as social justice within the nation.''')
    elif 'president of nigeria in 1993-1998' in command:
        sound('''General Sani Abacha. Shortly after overthrowing President Shonekan, Abacha issued a decree that essentially gave his government absolute power and immunity to prosecution. Abacha was involved with the 1966 counter-coup, the 1983 military coup as well as the 1985 coup, and he led the 1993 military coup against the interim government.
              Abacha's military legacy is one of successful coup attempts. His political legacy rests upon his remarkable economic achievements, which seem to overshadow some of the more controversial aspects of his government such as human rights abuses and corruption. Abacha managed to increased Nigerian foreign reserves from $494 million in 1993 to $9.6 billion by the middle of 1997
              Abacha also reduced the debt of Nigeria from $36 billion in 1993 to $27 billion in 1997. Abacha died mysteriously in 1998 and many Nigerians celebrated his death.''')
    elif 'president of nigeria in 1998-1999' in command:
        sound('''General Abdulsalami Abubakar. Although Abubakar was reluctant to accept the leadership of Nigeria when Abacha passed away, Abubakar was sworn in on the 9th of June, 1998. At this time, Nigeria needed a leader of Abubakar's caliber to avoid plunging into civil conflict, as he was a peaceful man who had Nigeria's best interests at heart.
              Abubakar and his government created a new Nigerian constitution, which would be implemented once a democratically elected leader was in place. Shortly after he was sworn in, Abubakar promised to hold general elections and step down as leader of Nigeria within one year. Critics of military leadership doubted that he would keep this promise, but he did.''')
    elif 'president of nigeria in 1999-2007' in command:
        sound('''President Olusegun Obasanjo. Obasanjo had already led Nigeria as a military leader, but his election to the office of President in 1999 marked Nigeria's return to civilian rule. Obasanjo won 62% of the vote and his election day is now marked as Democracy Day, a public holiday in the country. In his first term in office, Obasanjo spent most of his time travelling abroad to reassure potential investors
              especially those in the USA and UK, that the oil industry was stable, and that Nigeria was a fair and democratic country. Obasanjo was granted a second term in office in 2003 by Nigerians, winning 61% of the vote and defeating former military leader Muhammad Buhari.''')
    elif 'president of nigeria in 2007-2010' in command or 'umar musa' in command:
        sound('''President Umaru Musa Yar'Adua. After the controversial elections of 2007, Yar'Adua was declared the winner and assumed the Presidential office of Nigeria. Former President Obasanjo endorsed his candidacy, as his record showed no signs of corruption and/or ethnic favoritism. While in office, Yar'Adua fell ill and was unable to uphold his Presidential duties.
              This led to him being absent from public life and a dangerous situation was arising in Nigeria. His powers were transferred to Vice President Goodluck Jonathan, who took over as an acting President during this time. Yar'Adua's legacy while in office was one of democracy, fairness, peace, and prosperity for Nigerians.''')
    elif 'president of nigeria in 2010' in command or 'president in 2011' in command or 'president in 2012' in command or 'president in 2015' in command:
        sound('''President Goodluck Jonathan. As Yar'Adua's Vice President, Jonathan was known for keeping a low profile, although as Vice President he was instrumental in negotiating with Nigerian militants to achieve stability. After becoming President due to the illness and death of Yar'Adua, Jonathan contested the 2011 Nigerian elections, winning the Presidency
              Jonathan implemented a major strategy to stabilize the power supply of Nigeria, as blackouts were costing the economy millions, if not billions of dollars. Jonathan was also considered by many to be a staunch opposition of Boko Haram, an Islamic militant group, even though his armed forces were not able to defeat the group that still operates today.
              Jonathan's legacy is one of contrast, he improved the lives of many Nigerians but at the same time his government was hopelessly corrupt.''')
    elif 'president of nigeria in 2015-Present' in command or 'president of nigeria' in command:
        sound('''President Muhammadu Buhari. Having contested in the previous Presidential election, Buhari was finally successful in his 2015 bid to become President. Sworn in on May 29, 2015, Buhari became the second ex-military leader to become a President of Nigeria. After being elected, Buhari was also known as a strong voice against Boko Haram
              urging Nigerians to put aside their differences in order to crush the Islamic insurgency. On the 6th of June, 2016, Buhari went to the United Kingdom to seek medical treatment for a persistent ear infection. Only time will tell if his legacy will remain one of human rights abuses during his first term in power or will
              become one of fighting and defeating Boko Haram which is terrorizing Nigeria.''')
    elif 'Who Was the First President of Nigeria' in command or 'first president nigeria' in command:
        sound("Doctor Nmandi Azikiwe was the first President of Nigeria after the country became a fully independent republic and Nigeria cut ties with Britain.")
    elif 'who is the vice president of nigeria' in command:
        sound("The Vice President of Nigeria is the second-in-command to the President of Nigeria in the Government of Nigeria. Officially styled Vice President of the Federal Republic of Nigeria, the Vice President is elected alongside the President in national elections. The office is currently held by Professor. Yemi Osinbajo.")


   
    elif 'who is the FCT minister' in command or 'FCT minister' in command:
        sound('''Ramatu Tijjani Aliyu (born 12 June 1970) is a Nigerian politician who hails from Kogi State, Nigeria. She is the Minister of State for Federal Capital Territory (FCT) appointed by president Muhammadu Buhari on August 21, 2019.
              Ramatu was previously the National Woman Leader of the All Nigeria Peoples Party (ANPP) later All Progressive Congress (APC) after the party and other political parties merged (2014 - 2018), She has supported the incumbent president Muhammadu Buhari during his presidential campaigns
              where she criticised the opposition candidate in 2019 election, Alhaji Atiku Abubakar of not bringing anything important to the development of the country while he was the vice president of Nigeria, and called on Nigerians not to expect anything from him as he has nothing to offer again.
              She was previously elected the president of the Council of African Political Parties.''')


    #NIGERIAN CABINET, MINISTERS
    elif 'who are the nigerian cabinates' in command or 'Cabinet of Nigeria' in command:
        sound('''The Cabinet of Nigeria is part of the Executive Branch of the Government of Nigeria. The Cabinet's role, as written in the Ministers' Statutory Powers and Duties (MISCELLANEOUS PROVISIONS) Act is to serve as an advisory body to the President of Nigeria.
             Members of the Cabinet are appointed and report to the President, who can dismiss them at will. The Cabinet currently oversees 24 Federal Ministries, each responsible for some aspect of providing government services
            as well as a number of parastatals government-owned corporations.''')
    elif 'minister of justice' in command or 'attorney general of nigeria' in command or 'minister justice' in command or 'who is the minister of justice' in command:
        sound("Abubakar Malami born 17 April 1967, is a Nigerian politician, lawyer and Senior Advocate of Nigeria SAN. He is Nigeria's immediate past Minister for Justice and Attorney General.")
    elif 'minister of foreign affairs' in command or 'minister affairs' in command or 'who is the minister of affairs' in command:
        sound("Geoffrey Jideofor Kwusike Onyeama born February 2, 1956 is Nigeria's Minister for Foreign Affairs. Onyeama was appointed Foreign Affairs Minister of Nigeria in November 2015 by President Muhammadu Buhari.")
    elif 'minister of finance' in command or 'nigerian minister of budget' in command or 'nigerian mister of national planning' in command or 'who is the minister of finance' in command:
        sound("Zainab Shamsuna Ahmed born 16 June 1960 is a Nigerian accountant.She is the current Minister of Finance, Budget and National Planning appointed on August 21, 2019 as President Muhammadu Buhari brought the two ministries under her as one,making her the de facto Minister of Economy")
    elif 'minister of defence' in command or 'minister defence' in command or 'defence minster' in command or 'who is the minister of defence' in command:
        sound("Bashir Salihi Magashi is a retired Nigerian Army Major General and current Defence Minister of Nigeria. He was appointed Governor of Sokoto State from August 1990 to January 1992 during the military regime of General Ibrahim Babangida.[1] He was appointed Nigeria's Minister of Defence by President Muhammadu Buhari on 21 August 2019")
    elif 'who is the minister of education' in command or 'minster education' in command or 'education minsiter' in command:
        sound("Adamu Adamu is a Nigerian accountant, writer, former journalist, public analyst and a Minister of Education. He was first appointed minister by President Muhammadu Buhari on November 2015, along with 35 others, when the president made his first major appointments.Before his appointment as minister,he was the secretary of Muhammadu Buharis transition committee.He was reappointed on 21 August 2019 as Minister of Education by President Muhammadu Buhari")
    elif 'who is the minister of industry' in command or 'nigerian minister of trade' in command or 'nigerian minister of investment' in command or 'minister industry' in command:
        sound("Richard Adeniyi Adebayo")
    elif 'minister of labor' in command or 'nigerian minister of employment' in command or 'minister labor' in command or 'who is the minister of labour' in command or 'who is the minister of labor' in command:
        sound("Dr. Chris Nwabueze Ngige (born 8 August 1952) is the current Minister of Labour and Employment (Nigeria), appointed to serve in two terms under President Muhammadu Buhari's regime. He was elected Senator for Anambra Central Constituency in April 2011.He was the governor of Anambra State in Nigeria from May 2003 to March 2006 under the People's Democratic Party (PDP),Chris Ngige is currently a member of the All Progressives Congress (APC)")
    elif 'minister of FCT' in command or 'abuja minister' in command or 'who is the abuja minister' in command:
        sound("Alhaji Muhammad Musa Bello, who hails from Adamawa state, was born on 8th January 1959. An old boy of the prestigious Barewa College, Zaria, the Minister is a graduate of Ahmadu Bello University (ABU), Zaria, where he obtained a B.Sc. in Management with bias for Banking and Finance in 1980 as well as an MBA in the same field.")
    elif 'minister of science and technology' in command or 'minister science' in command or 'minister technology' in command or 'who is the minister of science' in command:
        sound("Ogbonnaya Onu (born December 1, 1951) is a Nigerian politician, author and engineer. He was the first civilian governor of Abia state and the immediate past Minister of Science and Technology, Federal Republic of Nigeria.")
    elif 'minister of mines and steel development' in command or 'minister of mines' in command or 'who is the minister of steel' in command:
        sound("Arc. Olamilekan Adegbite flanked from left by the CEO, Chairman of Management Board of Russian State Geological Holding (ROSGEO), Mr. Sergey Gorkov and the President and Chairman of Afrexim Bank, Benedict Okey Oramah represented by Gerald Chilhota the signing of MoU for Scientific and Technical Cooperation in the field of Geosciences, in Sochi, Russia.")
    elif 'minister of interior' in command or 'interior minister' in command or 'who is the minister of interior' in command:
        sound("Rauf Adesoji Aregbesola (born May 25th 1957) is the current Minister of the Federal Ministry of Interior (Nigeria) and the 4th civilian governor of the state of Osun. A native of Ilesa, Osun State, Nigeria, Ogbeni Rauf Aregbesola as he is popularly called is married to Mrs. Sherifat Aregbesola. Born into a family of both Muslims and Christians, Aregbesola, a Muslim of deep faith, was completely immersed in the art of religious tolerance, which he will later exhibit so publicly, in his tenure as governor of the State of Osun.")
    elif 'minister of works and housing' in command or 'minister works' in command or 'minister housing' in command or 'who is the minister of works' in command:
        sound("Babatunde Raji Fashola, SAN (Yoruba: Babatunde Raji Fasholo; born 28 June, 1963) is a Nigerian lawyer and politician who is currently the Federal Minister of Works and Housing. He served two terms as Governor of Lagos State from May 29, 2007 to May 29, 2015.As a candidate of the Action Congress party, now known as the All Progressives Congress, Fashola succeeded Bola Ahmed Tinubu, on 14 April, 2007, and was sworn in on 29 May, 2007.Fashola was re-elected on 26 April, 2011.On November 11th 2015, he was appointed by President Muhammadu Buhari to be the Minister of Power, Works and Housing; he was reappointed Minister of Works & Housing on the 21st of August 2019.")
    elif 'minister of transportation in nigeria' in command or 'minister transportation' in command or 'who is the minister of transportation' in command or 'who is the transportation minister' in command:
        sound("Chibuike Rotimi Amaechi (born 27 May 1965) is a Nigerian politician who served as the fifth Governor of Rivers State from 2007 to 2015 and serves currently as the Nigerian Minister for Transportation")
    elif 'minister of niger delta' in command or 'minister niger delta' in command or 'who is the minsiter of niger delta' in command:
        sound("Chief Godswill Obot Akpabio, CON (born 9 December 1962), is a Nigerian lawyer and politician. He is the current Minister of Niger Delta, a former Senator of the Federal Republic of Nigeria and the Senate's Minority Leader.[2][3] He also served as Governor of Akwa Ibom State of Nigeria from May 29, 2007 to May 29, 2015.")
    elif 'minister of information and culture' in command or 'minister information and culture' in command or 'who is the minister of information' in command:
        sound("Lai Mohammed is the current Nigeria's Minister of Information and Culture. A Nigerian medical doctor, and former National Publicity Secretary of the All Progressives Congress (APC).")
    elif 'minister of aviation' in command or 'minister aviation' in command or 'who is the minister of aviation' in command:
        sound("Sen. Sirika Hadi was the Minister for Aviation of the Federal Republic of Nigeria. He is a former Member House of Representative, and assumed the Senator of the Federal Republic of Nigeria in 2011, where he represents Katsina North Senatorial District under the platform of Congress for Progressive Change. Sirika held the position of (Vice-Chairman) of the Millennium Development Goals (MDGs) Committee set by the Nigerian Senate.")

    elif 'how many states are in nigeria' in command or 'states do we have in nigeria' in command:
        sound("Nigeria is divided into states (Hausa: jiha, Igbo: ora, Yoruba: ipinle), federated political entities that share sovereignty with the federal government. There are 36 states bound together by a federal agreement. The Federal Capital Territory is not a state and under the direct control of the federal government. The states are further divided into a total of 774 Local Government Areas.Under the Nigerian Constitution, states have the power to ratify constitutional amendments.")
    elif 'local goverments in nigeria' in command or 'local goverment' in command:
        sound("Nigeria has 774 local government areas (L.G.As). Each local government area is administered by a Local Government Council consisting of a chairman who is the Chief Executive of the LGA, and other elected members who are referred to as Councillors. Each of the areas is further subdivided into wards with a minimum of ten and a maximum of fifteen for each area.")
        
    
    else:
        sound('Did you say' + command)
        recipen = myCommand()
        if 'yes' in recipen or 'yah' in recipen or 'of course' in recipen or 'yeah' in recipen or 'yea' in recipen:
            sound("I am sorry, I don't have this in my storage command but let me search.., wait a moment please..,as am going to read some few lines of your answer found on my browser.")
            sound(wikipedia.summary(command)[:500])
        else:
            sound('Waitiing for another voice command from you sir..')
            
        
            
def takephoto():
    date_string = str(datetime.datetime.now())
    
    #camera = picamera.PiCamera()
    #camera.resolution = (1600, 1200)
    #camera.sharpness = 100
    
    date_string = 'image'+date_string+'.jpg'
    date_string = date_string.replace(":", "")  # Strip out the colon from date time.
    date_string = date_string.replace(" ", "")  # Strip out the space from date time.
    print("TAKE PICTURE: " + date_string)
    print(date_string)
    #camera.capture('image.png')
    os.system("fswebcam -r 1600x1200 --no-banner image.jpg")
    #camera.close() # We need to close off the resources or we'll get an error.
    call([" cp /home/pi/image.jpg "+"/home/pi/"+date_string], shell=True)
    
def parse_response(json_response):
    #print(json_response)
        try:
        #print json.dumps(response, indent=4, sort_keys=True)   #Print it out and make it somewhat pretty.
                anger = json_response['responses'][0]['faceAnnotations'][0]['angerLikelihood']
                surprise = json_response['responses'][0]['faceAnnotations'][0]['surpriseLikelihood']
                sorrow = json_response['responses'][0]['faceAnnotations'][0]['sorrowLikelihood']
                blurr = json_response['responses'][0]['faceAnnotations'][0]['blurredLikelihood']
                joy = json_response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
                
                anger_string = (str(anger))
                surprise_string = (str(surprise))
                sorrow_string = (str(sorrow))
        # print(str(blurr))
                happy_string = (str(joy))
        
                print("Happy: " + happy_string)
                print("Angry: " + anger_string)
                print("Surprise: " + surprise_string)
                print("Sorrow: " + sorrow_string)
        #sound("You look pretty. . . . tired.  You must have an infant?")
                print("joy ="+happy_string)
                if(happy_string == "VERY_LIKELY"):
                        sound("You seem happy!  Tell me why you are so happy today!")
                elif(anger_string == "VERY_LIKELY"):
                        sound("Uh oh, you seem angry!  I have kids, please don't hurt me!")
                elif(surprise_string == "VERY_LIKELY"):
                        sound("You seem surprised!  ")
                else:
                        sound("You seem sad!  Would you like a hug from me?")
        
        except:
                sound("I am sorry, I can not see your face now. thank you!?")
    

def take_emotion():
    #takephoto() # First take a picture
    """Run a label request on a single image"""
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
    "requests":[
    {
        "image":{
        "content":image_content.decode('UTF-8')
      },
        "features":[
        {
        "type":"FACE_DETECTION",
        "maxResults":5
        }
      ]
    }
  ]
})
        response = service_request.execute()
        parse_response(response)

def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

#Slave Address 2
#address_2 = 0x05

def writeNumber(value):
    bus.write_byte(address, value)
    #bus.write_byte(address_2, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    # number = bus.read_byte(address)
    number = bus.read_byte_data(address, 1)
    return number 


def main():
    once = True
    #sound("Hello!  I  am  si bot AI assistant!")
    if once:
            os.system('amixer cset numid=3 1')
            os.system('amixer set PCM 100%')
            once = False
    sound("Hello!!  my name is ABU SEER, the intelligent Personal Assistant robot, I am Created in Department of Computer Engineering Control Lab of Ahmadu Bello University,Zaria!, How may I help you?")
    '''takephoto() # First take a picture
    """Run a label request on a single image"""

    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)


    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    take_emotion()
    #detect_faces('faces.png')'''
    

    '''for label in labels:
        print(label.description)
        sound(x+label.description)'''
        
    while True:
        if GPIO2.input(10) == GPIO2.HIGH:
            sound("Reboot button was pushed, rebooting now")
            print("Button was pushed!")
            call(['shutdown', '-r', 'now'], shell=False)
        GPIO.output(RGB1_R, 0)
        GPIO.output(RGB1_G, 0)
        GPIO.output(RGB1_B, 0)
        GPIO.output(RGB2_R, 0)
        GPIO.output(RGB2_G, 0)
        GPIO.output(RGB2_B, 0)
        assistant(myCommand())   
        
    
    

    
if __name__ == '__main__':
    
    
    

    main()
