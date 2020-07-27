import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser=argparse.ArguementParser()
parser.add_arguement("__page_num_max",help="enter numberof pages to parse",type=int)
parser.add_arguement("__dbname",help="enter the name of db",type=str)
args=parse.parse_args()
oyo_url="https//www.oyorooms.com/hotels-in-bangalore/?page="
page_num_Max=args.page_num_Max
scraped_info_list=[]
connect.connect(args.dbname)
for page_num in range(1,page_num_Max):
    url=oyo_url+str(page_num)
    print("GET Request for:"+url)
    req=requests.get(url)
    content=req.content
    soup=BeautifulSoup(content,"html.parser")
    all_hotels=soup.find_all("div",{"class":"hotelcardlisting"})
    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict["name"]=hotel.find("h3",{"class":"listinghoteldescription__hotelName"}).text
        hotel_dict["address"]=hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict["price"]=hotel.find("span",{"class":"listingprice__finalprice"}).text
        try:
            hotel_dict["rating"]=hotel.find("span",{"class":"hotelrating__ratingsummary"})
        except AttributeError:
            hotel_dict["rating"]=none
        parent_amenities_element=hotel.find("div",{"class":"amenitywrapper"})
        amenities_list=[]
        for amenity in parent_amenities_element.find_all("div",{"class":"amenitywrapper__amenity"}):
            amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())
        hotel_dict["amenities"]=','.join(amenities_list[:-1])
        scraped_info_list.append(hotel_dict)
        connect.insert_info_table(args.dbname,tuple(hotel_dict.values()))
        dataframe=pandas.DataFrame(scraped_info_list)
        print("creating csv file...")
        dataframe.to_csv("oyo.csv")
        connect.get_hotel_info(args.dbname)
                                    
            

    
