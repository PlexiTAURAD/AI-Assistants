import cohere
from cohere.responses.classify import Example
import os
key = os.environ.get(KEY)
if key is None:
    raise ValueError("The COHERE_API_KEY environment variable is not set.")

co = cohere.Client(key)

### DATA ###
warranty_data=[Example("No I dont have warranty", "N"), Example("I used to but not anymore", "N"), 
               Example("It expired last month", "N"), Example("I will in a month", "N"), 
               Example("Yes I do", "Y"), Example("Just got it last month", "Y"), Example("I do", "Y"), 
               Example("I was planning on getting it next month", "N")]
classify1 = [
    Example("Hello, my laptop isnt connecting to the internet","0"),
    Example("My laptop keeps crashing","0"),
    Example("Why isnt my phone turning on?","0"),
    Example("How do I download apps","0"),
    Example("How do I upgrade my windows software?","0"),
    Example("What is the best laptop you are selling?","1"),
    Example("What are the device specifications for this phone?","1"),
    Example("Does this laptop have an HD display?","1"),
    Example("What is the camera quality in this phone?","1"),
    Example("Is this laptop good for gaming?","1"),
    Example("Hello I had ordered a laptop, when will I receive it?","2"),
    Example("I would like to cancel my order","2"),
    Example("My order still hasnt been delivered yet","2"),
    Example("I was supposed to recieve my order today, why did i not get it yet?","2"),
    Example("Can you change the address for the order? I will be outside","2"),
    Example("I want to return my product","3"),
    Example("Are there any exhange offers available for this product?","3"),
    Example("This product sucks and I want to return it","3"),
    Example("This product arrived broken, I dont want this","3"),
    Example("This product is misleading, I dont want it","3"),
    Example("Why was I charged extra?","4"),
    Example("Are loan options availabe for this device?","4"),
    Example("I would like to update my billing information","4"),
    Example("Can you send bills to a new address instead?","4"),
    Example("My account was debited despite the billing period being over","4"),
    Example("My device is broken, where can I fix it","5"),
    Example("How much will it cost to fix my phone","5"),
    Example("Where can I check my warranty?","5"),
    Example("I would like to extend my warranty","5"),
    Example("How much will a repair cost if I dont have warranty?","5"),
    Example("The laptop speakers are terrible","6"),
    Example("Great device! I loved it","6"),
    Example("Your products are awful","6"),
    Example("This is the best phone I ever had","6"),
    Example("Please just close down your company","6")
]

classify_warr = [
    Example("No I dont have warranty",0),
    Example("I used to but not anymore",0),
    Example("It expired last month",0),
    Example("I will in a month",0),
    Example("Yes I do",1),
    Example("Just got it last month",1),
    Example("I do",1)
]

#IMPORTANT VARIABLES
final_cat = "" #Category chosen by user
final_warr = "This information is unavailable" #If user has warranty
final_feel = "This information is unavailable" #How the user felt

first_input = input("Enter your Query: ")
inputt = first_input
tru_input = [inputt]
response = co.classify(
    model = "large",
    inputs = tru_input,
    examples= classify1
)
list = [] #This list will be used to summarise the whole interaction

tru_response = response.classifications[0].prediction #Getting the prediction with the highest confidence
list.append(tru_response) 
print(tru_response)

a = tru_input  
if list[0] == '0' or list[0] == '1':
    global tec_gen
    tec_gen = co.generate(
        model = "command-xlarge-nightly",
        prompt = a[0],        
        max_tokens=300,
        stop_sequences= ['--'],
        temperature=0.9,
        num_generations= 1)
    print(tec_gen.generations[0].text)
elif list[0] == '4' or list[0] == '3':
    print("Thankyou for connecting, based on your query we will now connect you to an agent who will further assist you")
elif list[0] == '5':
    user_input = input("Do you have warranty?")
    warranty = co.classify(
    model='large',
    inputs= [user_input],
    examples= warranty_data
    )
    if warranty == '0': # 0 means the user doesnt have any warranty
        print("That's okay. You can visit our stores to get your device repaired, I will connect you to an agent to calculate the cost")
        final_warr = "The user does not have warranty"
    else:
        print("Alright, you can come to our store or get a repairman to visit you and get your device repaired free of cost")
        final_warr = "The user has warranty"
elif list[0] == '6':
    responsenex = co.classify(
    model='large',
    inputs= [input],
    examples=[Example("Great product, I loved it", "8"), Example("Thankyou for being so awesome", "8"), Example("Absolute trash", "9"), Example("This really sucked", "9"), Example("I hope your company burns", "9"),]
    )
    feelings = responsenex.classifications[0].prediction
    if feelings == '8':
        print("Thankyou for your valuable feedback! We will ensure you continue to recieve quality products from us!")
        final_feel = "The user is happy with the company"
    elif feelings == '9':
        print("We are sorry to hear that, please contact us at greivances@lenuwu.com with more details")
        final_feel = "The user is unhappy with the company"
    

#implementation of text map   
category = ""
response_map = {'0': "Technical support", '1': "Product information", '2': "Order Inquiries", '3': "Returns and Exchanges", '4': "Billing and account issues", '5': "Warranty and repair", '6':"Complaints and feedback"}
print(list)
for i in list:
    category = response_map.get(i, "")
    final_cat = "The user contacted the " + category + " department \n"
print(final_cat)
print("Warranty: " + final_warr + "\n")
print("User rating: " + final_feel)
