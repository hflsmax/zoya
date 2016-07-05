from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse

def choice_without_id(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    print "no id"
    return render(request, 'saving_app/voya-choices.html')

def choice(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    clicks = request.GET.get("clicks")
    if (clicks == None):
        clicks = ""
    return render(request, 'saving_app/voya-choices.html',
                    {"user_id": user_id, "name": name, "clicks": clicks})

def set(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    user_id = request.GET.get("user_id")
    name = request.GET.get("name")
    try:
        clicks = request.GET.get("clicks")
    except Exception, e:
        print str(e)
        clicks = ""
    return render(request, 'saving_app/voya-set.html',
                    {"user_id": user_id, "name": name, "clicks": clicks})

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
            "set_time": 0
        })

    clicks = request.GET.get("clicks")
    if (clicks != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$set": {
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

    set_time = request.GET.get("set_time")
    if (set_time != None):
        db.user_data.update_one(
            {"user_id": user_id}, {
                "$inc": {
                    "set_time": float(set_time)
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
