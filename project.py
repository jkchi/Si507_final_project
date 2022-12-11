#!/usr/bin/env python
# coding: utf-8

# In[1]:


def get_top_200_population_city_cache():
    dump_dict ={}
    url_city = "https://www.michigan-demographics.com/cities_by_population"
    page = requests.get(url_city)
    soup = BeautifulSoup(page.content, 'html.parser')
    city_table = soup.find_all("table", class_="ranklist")
    city_list = [] 
    for i in city_table: 
        name = i.find_all('td')
        for j in name:
            if re.search(r'[~^0-9]',j.text) != None:
                pass
            else:
                text = re.sub('\n','',j.text)
                text = re.sub('          ','',text)
                text = re.sub('      ','',text)
                text = re.sub(' city','',text)
                text = re.sub(' City','',text)
                city_list.append(text)
    top200_city_population = city_list[0:200]
    dump_dict["city_list"] = top200_city_population        
    with open("city.json", "w") as outfile:
        json.dump(dump_dict, outfile)


# In[2]:


def get_restaurant(location,offset):
    url='https://api.yelp.com/v3/businesses/search'
    headers = {
    "accept": "application/json",
    "Authorization": yelp_key
    }
    params = {'term':'restaurants','location':str(location) + "Michigan","radius" : 20000,"limit":50              ,"offset":offset,"locale":"en_US"}

    response = requests.get(url, params=params, headers=headers)
    result = json.loads(response.text)["businesses"]
    return (result)


# In[3]:


class location: 
    def __init__(self, name="None",price_tree = []):
        self.name = name
        self.price_tree = price_tree
    def __str__ (self):
        return "location : " + self.name     


# In[4]:


class price: 
    def __init__(self,name="None",rest_tree = []):
        self.name = name
        self.rest_tree = rest_tree
    def __str__ (self):
        return "price : " + self.name


# In[5]:


class restaurant:
    def __init__(self, name="None",price= "None",review_count="None",rating = "None",categories = "None" ,id_res= 'None', city="None", location="None",                 cord = 'None',url = "None",json = None):
        if json != None:
            self.name = json['name']
            try:
                self.price = json['price']
            except:
                self.price = "None"
            self.review_count = json['review_count']
            self.rating = json['rating']
            self.categories = []
            for tag in json['categories']:
                self.categories.append(tag["title"])
            self.id_res = ['id_res']
            self.city = json['location']['city']
            self.location = ""
            for item in json['location']["display_address"]:
                self.location = self.location + item
            self.cord = json['coordinates']
            self.url = json['url']
        else:
            self.name = name
            self.price = price
            self.review_count = review_count
            self.rating = rating
            self.categories = categories
            self.id_res = id_res
            self.city = city
            self.location = location
            self.cord = cord
            self.url = url
    
    def get_categories(self,categories):
        if categories == "None":
            return None
        else:
            str_cate = ""
            for i in categories:
                str_cate = str_cate + i + "; "
        return str_cate
    
    def __str__ (self):
        return "name : " + self.name +"\n"+ "price : " + self.price +"\n"+  "review_count : " + str(self.review_count) +"\n"+ "rating : " + str(self.rating) +"\n"+ "categories : " + self.get_categories(self.categories) +"\n"+ "url : " + self.url 
                
        


# In[6]:


def tree_build_with_cache(city_list,cache_file):
    f = open(cache_file)
    cache_file = json.load(f)
    f.close()
    
    tree_root = []
    for city in city_list:
        
        price_1_node = price(name = "$",rest_tree=[])
        price_2_node = price(name = "$$",rest_tree=[])
        price_3_node = price(name = "$$$",rest_tree=[])
        price_4_node = price(name = "$$$$",rest_tree=[])
        price_5_node = price(name = "NA",rest_tree=[])
        
        cache_file
        rest_list_json = cache_file[str(city)]
        
        for rest_item_json in rest_list_json:
            rest_node = restaurant(json = rest_item_json)
            if  rest_node.price ==  "$":
                price_1_node.rest_tree.append(rest_node)
            elif rest_node.price == "$$":
                price_2_node.rest_tree.append(rest_node)
            elif rest_node.price == "$$$":
                price_3_node.rest_tree.append(rest_node)
            elif rest_node.price == "$$$$":
                price_4_node.rest_tree.append(rest_node)
            elif rest_node.price == "None":
                price_5_node.rest_tree.append(rest_node)
        
        city_node = location(name = city)
        city_node.price_tree = [price_1_node,price_2_node,price_3_node,price_4_node,price_5_node]
        tree_root.append(city_node)
    return tree_root


# In[7]:


def cache_rest_data(city_list):
    dump_dict ={}
    for city in city_list:
        temp_list = []
        for offset in range(0,300,50):
            rest_list_json = get_restaurant(city,offset)
            if rest_list_json == []:
                break
            else:
                temp_list = temp_list + rest_list_json
        dump_dict[str(city)] = temp_list
            
    with open("restaurant.json", "w") as outfile:
        json.dump(dump_dict, outfile)
            


# In[8]:


def load_city(city_file):
    f = open(city_file)
    cache_file = json.load(f)
    f.close()
    return(cache_file["city_list"])


# In[9]:


def question(city_list):
    
    print("Hello! Welcome to the restaurant recommendation app! I will try to give you some great dining choices in Michigan!")
    print("First please answer some questions.")
    print()
    print('Here are some more populated city.')
    print("Detroit; Grand Rapids; Sterling Heights;Ann Arbor; Lansing")
    
    while True:
        print("Please tell me the city you are at?")
        print("Please captitallize the first letter of each word of the city.")
        city_answer = input('Your Location: ')
        print()
        if city_answer not in city_list:
            print('City not found, maybe you can try the township of the city.')
            print("Please captitallize the first letter of the township name and add township in the end.")
        else:
            break
            
    while True:
        print('What is the your price range for the meal?')
        print("You can enter one to four dollar sign.")
        price_answer = input('Your Budget: ')
        
        if price_answer != "$" and price_answer != "$$" and price_answer != "$$$" and price_answer != "$$$$":
            print("\n")
            print("Please try again")
        else:
            break
    print('\n')        
    print('What cuisine or kind of food you are interested in?')
    print('Here is some example: American; Asian; Italian; Mexican; Chinese; Middle Eastern; Korean')
    print('Here is More example: Breakfast; Pizza; Cafes; Sushi')
    print('Please try to use a single word')
    interest_answer = input('Your interest: ').title()

  
    while True:
        print("\n")
        print('What is the minimal rating score you can accept?')
        print("You can input from 1 to 5")
        score_answer = input('Your score: ')
        try:
            score_answer = float(score_answer)
            if score_answer < 1 or score_answer > 5:
                print('Please input a valid score')
            else:
                break
        except:
            print('Please input a valid score')
            
       
    print("\n")
    print('If you want to know the distance from the restaurants to you location, please enter your street address.')
    print('Else you can enter N to skip the part')
    location_street_answer = input("Your stree address: ")
    if "N" in location_street_answer:
        pass
    else:
        location_street_answer = location_street_answer + "," + city_answer + ",MI"
    
    return [city_answer,price_answer,interest_answer,score_answer,location_street_answer]


# In[10]:


def search(question_answer,tree_root):
    result_rest = []
    for city_node in tree_root:
        if city_node.name == question_answer[0]:
            break
    price_tree = city_node.price_tree[len(question_answer[1])-1]
    for rest_node in price_tree.rest_tree:
        if question_answer[2] in str(rest_node.categories) and rest_node.rating >= question_answer[3]:
            result_rest.append(rest_node)
    if len (result_rest) >= 20:
        return(result_rest[0:20])
    else:
        return(result_rest)


# In[11]:


def driving_dist_cal(start,stop):
    key = google_map.key
    url = "https://maps.googleapis.com/maps/api/directions/json?"

    params={
            "origin" : start,
             "destination" : stop,
             "key" :key}
    headers={}

    response = requests.request("GET", url, headers=headers, params=params)
    result = json.loads(response.text)
    if result["status"] == 'NOT_FOUND':
        return "route not found"
    else: 
        return(result["routes"][0]["legs"][0]["distance"]["text"])


# In[12]:


def route_find(start,stop):
    url = "https://www.google.com/maps/dir/?api=1"

    params={
            "origin" : start,
             "destination" : stop}
    headers={}

    response = requests.request("GET", url, headers=headers, params=params)
    
    return(response.url)


# In[13]:


if __name__ == '__main__':
    
    import os
    import json
    import requests
    import google_map
    if not os.path.exists("city.json"):
        from bs4 import BeautifulSoup
        import re
        get_top_200_population_city_cache()
        city_list = load_city("city.json")
    else:
        city_list = load_city("city.json")

    if not os.path.exists("restaurant.json"):
        print("the cache process is about ten to fifteen mintues")
        f = open("API.txt", "r")
        yelp_key = f.readline()
        f.close()
        cache_rest_data(city_list)
        print("cache complete")
        tree_root = tree_build_with_cache(city_list,"restaurant.json")
    else:
        tree_root = tree_build_with_cache(city_list,"restaurant.json")
        
    while True:
        question_answer = question(city_list)
        rest_result = search(question_answer,tree_root)
        max_len = len(rest_result)
        
        if question_answer[4] == "N":
            if max_len <= 10:
                for index in range(max_len):
                    print(rest_result[index])
            else:
                for index in range(0,10):
                    print(rest_result[index])
                
            more_result_answer  = input("DO you want more result;enter YES to see more")
            if more_result_answer == "YES":
                for index in range(10,max_len):
                    print(rest_result[index])
                    
        else:
            if max_len <= 10:
                for index in range(max_len):
                    print(rest_result[index])
                    print("Driving Distance:")
                    print(driving_dist_cal(question_answer[4],rest_result[index].location))
                    print("Google Map Route")
                    print(route_find(question_answer[4],rest_result[index].location))
                    print("\n")
                    print("\n")

            else:
                for index in range(0,10):
                    print(rest_result[index])
                    print("Driving Distance:")
                    print(driving_dist_cal(question_answer[4],rest_result[index].location))
                    print("Google Map Route")
                    print(route_find(question_answer[4],rest_result[index].location))
                    print("\n")
                    print("\n")
            
                more_result_answer  = input("DO you want more result;enter YES to see more ")
                if more_result_answer == "YES":
                    for index in range(10,max_len):
                        print(rest_result[index])
                        print("Driving Distance:")
                        print(driving_dist_cal(question_answer[4],rest_result[index].location))
                        print("Google Map Route")
                        print(route_find(question_answer[4],rest_result[index].location))
                        print("\n")
                        print("\n")
    
    
        another_run = input("Do you want to search for another choice; Enter NO to exit; Any other thing to continue")
        if another_run == "NO":
            print("Goodbye")
            break
        
    
    

