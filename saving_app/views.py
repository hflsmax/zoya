from django.shortcuts import render

def choice_without_id(request):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    print "no id"
    return render(request, 'saving_app/voya-choices.html', {"user_id": "no id"})

def choice(request, user_id):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    print "have id"
    return render(request, 'saving_app/voya-choices.html', {"user_id": user_id})

def set(request, user_id):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    return render(request, 'saving_app/voya-set.html', {"user_id": user_id})
