from django.shortcuts import render

def first_page(request, user_id):
    # return render(request, 'saving_app/voya-choices.html', {'user_id': user_id})
    return render(request, 'saving_app/voya-choices.html')
