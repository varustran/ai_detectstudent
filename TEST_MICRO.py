# import speech_recognition
# # khởi tạo
# ai_brain = " " # Ban đầu nó chưa được học gì cả nên cũng chưa có thông tin
# ai_ear = speech_recognition.Recognizer() # nghe người dùng nói
# you = "" # Lời nói người dùng
# print("Khởi động mic")
# with speech_recognition.Microphone() as mic:
#     print("AI: Đang nghe")
#     audio = ai_ear.record(mic, duration = 5)
#     try:
#         # Nghe giọng nói của người Việt
#         you = ai_ear.recognize_google(audio, language = 'vi-VN')
#         print(you)
#     except:
#         print("Tôi không hiểu bạn noi gi")

import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

import folium

from opencage.geocoder import OpenCageGeocode

# taking input the phonenumber along with the country code
number = input("Enter the PhoneNumber with the country code : ")
# Parsing the phonenumber string to convert it into phonenumber format
phoneNumber = phonenumbers.parse(number)

# Storing the API Key in the Key variable
Key = "fa91a4da0a434e109178c334047f2f37"  # generate your api https://opencagedata.com/api

# Using the geocoder module of phonenumbers to print the Location in console
yourLocation = geocoder.description_for_number(phoneNumber, "en")
print("location : " + yourLocation)

# Using the carrier module of phonenumbers to print the service provider name in console
yourServiceProvider = carrier.name_for_number(phoneNumber, "en")
print("service provider : " + yourServiceProvider)

# Using opencage to get the latitude and longitude of the location
geocoder = OpenCageGeocode(Key)
query = str(yourLocation)
results = geocoder.geocode(query)

# Assigning the latitude and longitude values to the lat and lng variables
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']

# Getting the map for the given latitude and longitude
myMap = folium.Map(loction=[lat, lng], zoom_start=9)

# Adding a Marker on the map to show the location name
folium.Marker([lat, lng], popup=yourLocation).add_to(myMap)

# save map to html file to open it and see the actual location in map format
myMap.save("Location.html")