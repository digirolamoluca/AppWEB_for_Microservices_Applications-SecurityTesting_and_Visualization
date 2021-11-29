import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from . import macm
import datetime



# Create your views here.
def app(request):
    #print(request.POST)
    return render(request, 'app/base.html')

def generate_macm(request):

    now = datetime.datetime.now()
    x=now.strftime('%d-%m-%YT%H:%M:%S')

    payload=request.POST
    #print(payload)
    file=request.FILES['file']

    fs = FileSystemStorage(location="./docker_compose")

    relativePath="./docker_compose/"+file.name
    if os.path.exists(relativePath):
        os.remove(relativePath)
    filename = fs.save(file.name, file)

    if request.method == 'POST':
        macm.dockercompose_WriteTo_macmFile(relativePath,payload['app_id'],payload['application_name'])
    else:
        print("POST ERROR")


    response = HttpResponse(open("./"+payload['application_name']+".macm", 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename='+payload['application_name']+'_'+x+'.macm'
    return response



def customize(request):
    return render(request, 'app/customize.html')

