from django.shortcuts import render
import json
from .my_library import insertIMAGEDATA, retrieveIMAGEDATA

def main_page(request):
        if request.method == 'POST':
                insertIMAGEDATA(request.FILES['upload'].read())
                temp = retrieveIMAGEDATA()
                json_array = json.dumps(temp)    
                return render(request,'front_page.html',{'json_array':json_array})
        else:
                temp = retrieveIMAGEDATA()
                json_array = json.dumps(temp)    
                return render(request,'front_page.html',{'json_array':json_array})