# Si507_final_project
This is for the fianl project of si507. Try to build a restaurant recommendation script. 

The script requires the following packages.
1.os 2.requests 3.google_map 4.BeautifulSoup

API keys
The script used the following api keys.
1. Yelp fusion
By creating a yelp account and a new project, api key will be generated.
Related reading: https://fusion.yelp.com/
After acquiring the key, create API.txt and paste "Bearer " + api key inside.
example: Bearer _08Up8W9Ehqxxxxxx
2. Google Map api
The route api is used. You need to create a account add a payment method to use the api. 
Related reading: https://developers.google.com/maps
After acquiring the key, create a google_map.py and create a varible called key and assigne its value to be the api key.
example: key = "key = "AIzaSyA_XXXXXXX"

Instruction
Interaction and Presentation Plans
The command line will present the final result. The app asks several questions and returns several dining recommendations for the city you are currently in. 

Questions and tips
Q1:
Please tell me the city you are in.
A1:
In the answer, please capitalize the first letter of each word.
For example, Ann Arbor instead of ann arbor; Detriot instead of detriot.
If the script return city not found, you could try the name of the township to which the city belongs.
In the answer, please capitalize only the first letter of the first word of the township and add township at the end.
For example, Clinton charter township instead of Clinton Charter Township or Clinton Charter township.

Q2:
What is your price range for the meal?
A2:
You can enter one to four dollar signs, such as $ or $$$$.

Q3:
What cuisine or kind of food are you interested in?
A3:
Please use a single word in the answer, such as American, Asian, Italian, Breakfast, and Pizza.

Q4:
What is the minimal rating score you can accept?
A4:
Please answer it using a digit from 1 to 5. 

Q5:
Please enter your street address if you want to know the distance from the restaurants to your location. Else you can enter N to skip the part.
A5: 
Answer example,500 S State St or N, 105 S State St(Umich School of information)
Please note the script does not support a search of the location outside the city choice in question 1. 

Data stuctutre 
After the cache file was found, a tree root was created. Within the root, for each city, a location class was formed with an empty price tree. Then five price tree was created for each city node, representing five price classes(different price levels) with an attribute of the restaurant tree. For each restaurant record, a restaurant class was created with characteristics of restaurant information such as location, price, etc. Then restaurant node will be added to the price tree based on its price attribute. Finally, these price trees will be added to the corresponding location class. 



