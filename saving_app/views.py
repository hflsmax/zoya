from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse, HttpResponseNotFound
from django.http.request import QueryDict
import json
import os
import pandas as pd
from django.conf import settings
import pdb

def choice_without_id(request):

    request.GET = request.GET.copy()
    request.GET.update({'user_id': 1234, 'name': 'Max', 'intervention': 1})
    return choice(request, alert="""alert(\"You shouldn\'t be here.\")""")

def choice(request, alert=""):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    try:
        user_id = request.GET.get("user_id")
        name = request.GET.get("name")
        intervention = int(request.GET.get("intervention"))
    except:
        return HttpResponseNotFound("<h1>Please specify correct paramters. These are user_id, name and intervention.</h1>")
    if (intervention == 1):
        chooseText = ("I want to enroll with other choices.", "Note: This enrollment will cancel your scheduled automatic enrollment.")
        defaultText = ("Let my scheduled automatic enrollment go through.", "")
        optoutText = ("I do not wish to enroll.", "")
    elif (intervention == 2):
        chooseText = ("Do it Myself", "I want to enroll with other choices")
        defaultText = ("Do it for Me", "Let my scheduled auto-enrollment go through")
        optoutText = ("I Don't Want to Save", "I want to cancel my auto-enrollment")
    elif (intervention >= 3 and intervention <= 17):
        chooseText = ("I want to enroll at a different rate.", "I want to personalize my enrollment by selecting a different savings rate.")
        defaultText = ("I want to confirm my automatic enrollment.", "I want my auto-enrollment to go through at the savings rate chosen by my employer.")
        optoutText = ("I do not want to enroll.", "I want to cancel my auto-enrollment and not save at this time.")
    else:
        return HttpResponseNotFound("<h1>Currently only support intervention from 1 to 17.</h1>")

    # Extra text
    if (intervention >= 14):
        extraText = "You will be automatically enrolled at a contribution rate of 6 percent."
    else:
        extraText = ""

    # Orientation
    if (intervention >= 9 and intervention <= 10):
        grid = "col-sm-4 col-sm-offset-4"
    else:
        grid = "col-sm-4"

    chooseAttr = "id=others"
    defaultAttr = """id="auto" onclick="$('#myModal2').modal({backdrop:'static'}, 'toggle');" """
    optoutAttr = """id="no" onclick="$('#myModal').modal({backdrop:'static'}, 'toggle');" """
    optionsAttr = [None]*3
    optionsText = [None]*3
    # Option position and text
    if (intervention in [1,2,3,10,11,12,13,14,15,16,17]):
        optionsAttr = [chooseAttr, defaultAttr, optoutAttr]
        optionsText = [chooseText, defaultText, optoutText]
    elif (intervention in [4, 9]):
        optionsAttr = [defaultAttr, chooseAttr, optoutAttr]
        optionsText = [defaultText, chooseText, optoutText]
    elif (intervention in [5]):
        optionsAttr = [defaultAttr, optoutAttr, chooseAttr]
        optionsText = [defaultText, optoutText, chooseText]
    elif (intervention in [6]):
        optionsAttr = [chooseAttr, optoutAttr, defaultAttr]
        optionsText = [chooseText, optoutText, defaultText]
    elif (intervention in [7]):
        optionsAttr = [optoutAttr, chooseAttr, defaultAttr]
        optionsText = [optoutText, chooseText, defaultText]
    elif (intervention in [8]):
        optionsAttr = [optoutAttr, defaultAttr, chooseAttr]
        optionsText = [optoutText, defaultText, chooseText]

    # Option colors
    color = [""]*3
    if (intervention in [11, 15]):
        color = ["", "", "red"]
    elif (intervention in [12, 16]):
        color = ["green", "yellow", "red"]
    elif (intervention in [13, 17]):
        color = ["yellow", "green", "red"]

    return render(request, 'saving_app/voya-choices.html',
                    {"user_id": user_id, "name": name, "optionsText": optionsText,
                    "intervention": intervention, "extraText": extraText,
                    "grid": grid, "optionsAttr": optionsAttr, "color": color, "alert": alert})

def set1(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    intervention = int(request.GET.get("intervention"))
    return render(request, 'saving_app/voya-set1.html',
                    {"user_id": user_id, "name": name, "intervention": intervention})

def set2(request):
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    contri = request.GET.get("contri")
    age = request.GET.get("age")
    salary = request.GET.get("salary")
    savings = request.GET.get("savings")
    intervention = int(request.GET.get("intervention"))
    if (contri == None):
        contri = -1
    return render(request, 'saving_app/voya-set2.html',
                    {"user_id": user_id, "name": name, "contri": contri,
                    "age": age, "salary": salary, "savings": savings, "intervention": intervention})

def lookup(request):
    age = int(request.GET.get("age"))
    salary = int(request.GET.get("salary"))
    savings = int(request.GET.get("savings"))
    csv_file = os.path.join(settings.BASE_DIR, "saving_app/lookup.csv")
    lk = pd.read_csv(csv_file)
    # The largest element which is smaller than the query
    uni_ages = lk.Age.unique()
    age_thre = uni_ages[age >= uni_ages]
    if (len(age_thre) == 0):
        uni_ages.sort()
        age_thre = uni_ages[0]
    else:
        age_thre.sort()
        age_thre = age_thre[-1]
    # The largest element which is smaller than the query
    uni_salaries = lk.Salary.unique()
    salary_thre = uni_salaries[salary >= uni_salaries]
    if (len(salary_thre) == 0):
        uni_salaries.sort()
        salary_thre = uni_salaries[0]
    else:
        salary_thre.sort()
        salary_thre = salary_thre[-1]
    # The largest element which is smaller than the query
    uni_savings = lk.Savings.unique()
    savings_thre = uni_savings[savings >= uni_savings]
    if (len(savings_thre) == 0):
        uni_savings.sort()
        savings_thre = uni_savings[0]
    else:
        savings_thre.sort()
        savings_thre = savings_thre[-1]
    small_lk = lk[(lk['Age'] == age_thre) & (lk['Salary'] == salary_thre) & (lk['Savings'] == savings_thre)]
    lk_dict = {}
    for row in small_lk.iterrows():
        lk_dict[row[1]['Rate']] = {}
        lk_dict[row[1]['Rate']]['target'] = row[1]['Target']
        lk_dict[row[1]['Rate']]['need'] = row[1]['Need']
        lk_dict[row[1]['Rate']]['gap'] = row[1]['Gap']

    data = json.dumps(lk_dict)
    return HttpResponse(data, content_type='application/json')




def set3(request):
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    contri = request.GET.get("contri")
    age = request.GET.get("age")
    salary = request.GET.get("salary")
    savings = request.GET.get("savings")
    intervention = int(request.GET.get("intervention"))
    return render(request, 'saving_app/voya-set3.html',
                    {"user_id": user_id, "name": name, "contri": contri,
                    "age": age, "salary": salary, "savings": savings, "intervention": intervention})

def update(request):
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    client = MongoClient()

    # client = MongoClient("mongodb://<dbuser>:<dbpassword>@ds017985-a0.mlab.com:17985,ds017985-a1.mlab.com:17985/<dbname>?replicaSet=rs-ds017985")
    client = MongoClient(os.environ['MONGOLAB_OLIVE_URI'])

    # client = MongoClient("mongodb://heroku_8934f4g7:j254phhfmoh04ikpkl4ff9vp17@ds015325.mlab.com:15325/heroku_8934f4g7")
    db = client.get_default_database()
    cursor = db.user_data.find_one({"user_id": user_id})
    if (cursor == None):
        db.user_data.insert_one({
            "name": name,
            "user_id": user_id,
            "choice_time": 0,
            "set1_time": 0,
            "set2_time": 0,
            "set3_time": 0,
            "clicks": []
        })

    clicks = request.GET.get("clicks")
    if (clicks != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$push": {
                    "clicks": clicks
                }
            }
        )

    choice_time = request.GET.get("choice_time")
    if (choice_time != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$inc": {
                    "choice_time": float(choice_time)
                }
            }
        )

    set1_time = request.GET.get("set1_time")
    if (set1_time != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$inc": {
                    "set1_time": float(set1_time)
                }
            }
        )

    set2_time = request.GET.get("set2_time")
    if (set2_time != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$inc": {
                    "set2_time": float(set2_time)
                }
            }
        )

    set3_time = request.GET.get("set3_time")
    if (set3_time != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$inc": {
                    "set3_time": float(set3_time)
                }
            }
        )

    rate = request.GET.get("rate")
    if (rate != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$set": {
                    "rate": int(float(rate))
                }
            }
        )

    final_choice = request.GET.get("final_choice")
    if (final_choice != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$set": {
                    "final_choice": final_choice
                }
            }
        )

    intervention = request.GET.get("intervention")
    if (intervention != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$set": {
                    "intervention": intervention
                }
            }
        )

    return HttpResponse('')
