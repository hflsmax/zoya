from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse, HttpResponseNotFound
import json
import os
import pandas as pd
from django.conf import settings

def choice_without_id(request):
    return HttpResponseNotFound("<h1>You're not suppose to be here.</h1>")

def choice(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    try:
        user_id = request.GET.get("user_id")
        name = request.GET.get("name")
        intervention = int(request.GET.get("intervention"))
    except:
        return HttpResponseNotFound("<h1>Please specify correct paramters. These are user_id, name and intervention.</h1>")
    texts = [None] * 3
    if (intervention == 1):
        texts[0] = ("I want to enroll with other choices.", "Note: This enrollment will cancel your scheduled automatic enrollment.")
        texts[1] = ("Let my scheduled automatic enrollment go through.", "")
        texts[2] = ("I do not wish to enroll.", "")
    elif (intervention == 2):
        texts[0] = ("Do it Myself", "I want to enroll with other choices")
        texts[1] = ("Do it for Me", "Let my scheduled auto-enrollment go through")
        texts[2] = ("I Don't Want to Save", "I want to cancel my auto-enrollment")
    elif (intervention == 3):
        texts[0] = ("I want to enroll at a different rate.", "I want to personalize my enrollment by selecting a different savings rate.")
        texts[1] = ("I want to confirm my automatic enrollment.", "I want my auto-enrollment to go through at the savings rate chosen by my employer.")
        texts[2] = ("I do not want to enroll.", "I want to cancel my auto-enrollment and not save at this time.")

    return render(request, 'saving_app/voya-choices.html',
                    {"user_id": user_id, "name": name, "texts": texts, "intervention": intervention})

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
    client = MongoClient("mongodb://heroku_8934f4g7:j254phhfmoh04ikpkl4ff9vp17@ds015325.mlab.com:15325/heroku_8934f4g7")
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
    return HttpResponse('')
