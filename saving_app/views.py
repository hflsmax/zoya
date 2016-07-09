from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse, HttpResponseNotFound


def choice_without_id(request):
    return HttpResponseNotFound("<h1>You're not suppose to be here.</h1>")

def choice(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    return render(request, 'saving_app/voya-choices.html',
                    {"user_id": user_id, "name": name})

def set1(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    return render(request, 'saving_app/voya-set1.html',
                    {"user_id": user_id, "name": name})

def set2(request):
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    return render(request, 'saving_app/voya-set2.html',
                    {"user_id": user_id, "name": name})

def set3(request):
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    contri = request.GET.get("contri")
    return render(request, 'saving_app/voya-set3.html',
                    {"user_id": user_id, "name": name, "contri": contri})

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
