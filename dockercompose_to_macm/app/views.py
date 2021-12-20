import os
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from . import dockercompose_to_macmFile
from neo4j import GraphDatabase
import datetime
from .models import *
import re
import shutil

# Create your views here.


def app(request):

    total_appid = []
    macms=MACM.objects.all()
    for macmObj in macms:
        total_appid.append(macmObj.appId)
    total_appid_ordered=sorted(total_appid)
        #total_appid=list(dict.fromkeys(total_appid))

    return render(request, 'app/base.html',{
        'total_appid':total_appid_ordered
    })


def generate_macm(request):

    payload=request.POST
    yes_no=payload['yes_no']

    total_appid = []
    macms=MACM.objects.all()
    for macmObj in macms:
        total_appid.append(macmObj.appId)
    total_appid_ordered=sorted(total_appid)
    if(len(total_appid_ordered)==0):
        temp=0
    else:
        temp=total_appid_ordered[len(total_appid_ordered)-1]+1
    appid_choise=str(temp)


    try:
        file=request.FILES['file']
    except:
        error="Upload 'Docker Compose file' non valido. IL DOCKER COMPOSE FILE VA CARICATO SEMPRE! Riprova"
        return render(request, 'app/base.html',{
            'error':error,
            'total_appid':total_appid
        })

    if yes_no=="Crea":
        fs = FileSystemStorage(location="./docker_compose")
        #relativePath="./docker_compose/"+file.name
        relativePath="./docker_compose/"+str(appid_choise)+file.name
        if os.path.exists(relativePath):
            os.remove(relativePath)
        fs.save(str(appid_choise)+file.name, file)
        #filename = fs.save(file.name, file)




    application = payload['application_name']
    outputfolder = "./macms/"


    #name = []
    #type = []





    if request.method == 'POST':
        if application=="" and yes_no=="Crea":
            error2="Campo 'Application Name' non valido.Riprova"
            return render(request, 'app/base.html',{
            'error2':error2,
            'total_appid':total_appid
        })
        #if appid=="":
        #    error3="Campo 'App Id' non valido.Riprova"
        #    return render(request, 'app/base.html',{
        #    'error3':error3
        #})

         #definisco gli asset type da inserire nel dropdown menu
        asset_t = []
        assettype=Asset_Type.objects.all()
        for i in range(0,len(assettype),1):
            asset_t.append(assettype[i].asset_type)




        if yes_no=="Crea":
            nodes = dockercompose_to_macmFile.dockercompose_WriteTo_macmFile(outputfolder,relativePath,appid_choise,application,0,0)
            #alert_overwrite="MACM con appid:"+appid+" già presente. Il MACM precedente è stato sovrascritto"
            #obj_rm=MACM.objects.get(appId=total_appid[i])
            #obj_rm.delete()
            alist=[]
            for i in range(0,len(nodes),1):
                alist.append("")
            lista=zip(nodes,alist,alist,alist,alist,alist,alist)
            return render(request, 'app/base.html',{
            #'alert_overwrite':alert_overwrite,
            'lista':lista,
            'nodes' : nodes,
            'asset_t' : asset_t,
            'appid': appid_choise,
            'application': application,
            'outputfolder': outputfolder,
            'relativePath':relativePath,
            'yes_no':yes_no})

        #MACMobj=MACM(appId=appid_choise,application=application,components="",primaries="",secondaries="",asset_types="",dev_types="",custom_types="")
        #a=str(MACMobj.appId)
        #MACMobj.save()



        if yes_no=="Carica":
            print(payload)
            appid= payload['app_id']
            #for i in range(0,len(total_appid),1):
                #if a == str(total_appid[i]):
            alert_backup="Si è effettuato il backup del precedente MACM con appid: "+appid
            obj_backup=MACM.objects.get(appId=appid)
            alist=obj_backup.asset_types
            dlist=obj_backup.dev_types
            clist=obj_backup.custom_types
            components=obj_backup.components
            primaries=obj_backup.primaries
            secondaries=obj_backup.secondaries
            application=obj_backup.application
            #atype_backup=json.dumps(obj_backup.asset_types)
            #a=json.loads(atype_backup)
            #print(atype_backup[1])
            #dtype_backup=obj_backup.dev_types
            #ctype_backup=obj_backup.custom_types
            #print(alist)
            list=["'",",","[","]"]
            atype_backup="".join(i for i in alist if i not in list)
            dtype_backup="".join(i for i in dlist if i not in list)
            ctype_backup="".join(i for i in clist if i not in list)
            components_backup="".join(i for i in components if i not in list)
            primaries_backup="".join(i for i in primaries if i not in list)
            secondaries_backup="".join(i for i in secondaries if i not in list)
            #ctype_backup=" ".join(i for i in ctype_backup if i not in list)
            #print(atype_backup.split())
            alist=atype_backup.split()
            dlist=dtype_backup.split()
            clist=ctype_backup.split()
            components=components_backup.split()
            primaries=primaries_backup.split()
            secondaries=secondaries_backup.split()
            obj_backup.delete()
            lista=zip(alist,alist,dlist,clist,components,primaries,secondaries)
            print("appid:")
            print(appid)
            return render(request, 'app/base.html',{
            'components':components,
            'primaries':primaries,
            'secondaries':secondaries,
            'alert_backup':alert_backup,
            'nodes': alist,
            'lista':lista,
            'asset_t' : asset_t,
            'appid': appid,
            'application': application,
            'outputfolder': outputfolder,
            'file':file,
            'yes_no':yes_no})

        #alist=[]
        #for i in range(0,len(total_appid),1):
        #            alist.append("")
        #lista=zip(alist,alist,alist,alist,alist,alist,alist)


        #total_appid = []
        #macms=MACM.objects.all()
        #ind=0
        #for macmObj in macms:
        #    total_appid.append(macmObj.appId)
        #total_appid=list(dict.fromkeys(total_appid))


        #MACM.objects.filter(appId=100)
    #    for i in range(0,len(nodes),1):
    #        name.append(nodes[i].get_name())
    #        type.append(nodes[i].get_type())


    #return render(request, 'app/base.html',{
        #'lista':lista,
        #'nodes' : nodes,
        #'asset_t' : asset_t,
        #'appid': appid,
        #'application': application,
        #'outputfolder': outputfolder,
        #'relativePath':relativePath,
        #'yes_no':yes_no})

    #download:
    #response = HttpResponse(open("./"+payload['application_name']+".macm", 'rb').read())
    #response['Content-Type'] = 'text/plain'
    #response['Content-Disposition'] = 'attachment; filename='+payload['application_name']+'_'+x+'.macm'
    #return response


def customize_macm(request):
    payload=request.POST

    #print(payload)
    if request.method == 'POST':
        #print(payload.appid)
        print("customizemacm")
        print(payload)
        file=payload.getlist('file')
        file=file[0]
        yes_no=payload.getlist('yes_no')
        yes_no=yes_no[0]
        relativePath=payload.getlist('relativePath')
        relativePath=relativePath[0]
        outputfolder=payload.getlist('outputfolder')
        outputfolder=outputfolder[0]
        application=payload.getlist('application')
        application=application[0]
        appid=payload.getlist('appid')
        appid=appid[0]
        atype=payload.getlist('asset_type')
        dtype=payload.getlist('dev_type')
        ctype=payload.getlist('custom_type')

        print("file:")
        print(file)
        #for i in range(0,len(atype),1):
            #if(atype[i]=="?"):
            #    error4="Tutti i campi sono obbligatori non è possibile lasciare valori incogniti '?'"
            #    return render(request, 'app/base.html', {
            #        'error4': error4
            #    })

        components = []
        primaries = []
        secondaries = []
        #asset_types = []

        if yes_no=="Crea":
            nodes_customize=dockercompose_to_macmFile.dockercompose_WriteTo_macmFile(outputfolder,relativePath,appid,application,atype,dtype)

            for i in range(0,len(nodes_customize),1):
                components.append(nodes_customize[i].get_name())
                primaries.append(nodes_customize[i].get_primary())
                secondaries.append(nodes_customize[i].get_secondary())
                #asset_types.append(nodes_customize[i].get_type())

        if yes_no=="Carica":
            #$$$$$$$
            #dockercompose_to_macmFile.dockercompose_WriteTo_macmFile(outputfolder,relativePath,appid,application,atype,dtype)
            print("carica customize macm")
            print(payload)
            appid=payload.getlist('appid')
            appid=appid[0]
            print("ottenuto")
            print(appid)
            components=payload.getlist('components')
            components=components[0]
            primaries=payload.getlist('primaries')
            primaries=primaries[0]
            secondaries=payload.getlist('secondaries')
            secondaries=secondaries[0]
            dockercompose_to_macmFile.dockercompose_WriteTo_macmFile(outputfolder,"./docker_compose/"+appid+file,appid,application,atype,dtype)


        MACMobj_customize=MACM(appId=appid,application=application,components=components,primaries=primaries,secondaries=secondaries,asset_types=atype,dev_types=dtype,custom_types=ctype)
        MACMobj_customize.save()



    #return render(request,'app/pipeline.html',request.POST)
    return render(request,'app/settings.html',request.POST)
    #return render(request,'app/settings.html',{
    #             'appid':appid} )





#$$$$$$$$ return render(request,'app/settings.html',request.POST)

  #  return render(request, 'app/settings.html', {
  #      'appid':appid,
  #      'application':application,
  #      'outputfolder':outputfolder,
  #      'relativePath': relativePath
  #  })

def macm_to_neo4j(request):

    payload=request.POST
    #print("macm to neo4j")
    #print(payload)


    #definirle in setting.py:
    neo4jUsername = "neo4j"
    neo4jPassword = "123456789"

    #a=payload['appid']
    a=payload['appid']
    list=["'","[","]"]
    appid="".join(i for i in a if i not in list)


    #macmobj=MACM.objects.Get_or_Create.filter(appId=appid)

    macmobj=MACM.objects.get_or_create(appId=appid)
    application=macmobj[0].application
    file_cypher=open("./macms/"+application+appid+".macm","r")
    macm_string=file_cypher.read()
    macm_string_count="match (n{app_id:'"+appid+"'}) return count(n) as num_nodi"
    macm_string_remove="match (n{app_id:'"+appid+"'}) detach delete n"

    #aggiungi altre query_to_neo(macm_string,neo4jUsername,neo4jPassword,"bolt://localhost:7687")
    #dove in macm_string fai queste query (ovvero sostituisci macm_string con in seguenti valori):
    #match (n{app_id:'99'}) return count(n) se è maggiore di zero allora vuol dire che esiste
    #quindi lo elimino con altra query , ovvero match (n{app_id:'99'}) detach delete n


    if request.method == 'POST':


        count_node=query_to_neo(macm_string_count,neo4jUsername,neo4jPassword,"bolt://localhost:7687",appid)

        if count_node>0:
            query_to_neo(macm_string_remove,neo4jUsername,neo4jPassword,"bolt://localhost:7687",appid)
            query_to_neo(macm_string,neo4jUsername,neo4jPassword,"bolt://localhost:7687",appid)
            error8="MACM già presente con appid:"+appid+" su neo4j. Il MACM associato è stato sovrascritto"
            return render(request, 'app/settings.html',{
            'appid':appid,
            'error8':error8,
        })

        if count_node==0:
            query_to_neo(macm_string,neo4jUsername,neo4jPassword,"bolt://localhost:7687",appid)
            alert="MACM con appid:"+appid+" creato con successo"
            return render(request, 'app/settings.html',{
            'appid':appid,
            'alert':alert,
        })
        #successfull=query_to_neo(macm_string,neo4jUsername,neo4jPassword,"bolt://localhost:7687")

    #return render(request, 'app/settings.html')

    #return render(request, 'app/settings.html',{
    #    'appid':appid
    #})

def query_to_neo(query,neo4jUsername,neo4jPassword,urineo4j,application_id):

    graphDriver = GraphDatabase.driver(uri=urineo4j, auth=(neo4jUsername, neo4jPassword))
    session = graphDriver.session()
    a=session.run(query)
    if query=="match (n{app_id:'"+application_id+"'}) return count(n) as num_nodi":
        b=a.data()[0]
        graphDriver.close()
        return b['num_nodi']

def download(request):

    payload=request.POST
    ok="yes"
    a=payload['appid']
    list=["'","[","]"]
    appid="".join(i for i in a if i not in list)

    now = datetime.datetime.now()
    x=now.strftime('%d-%m-%YT%H:%M:%S')


    #appid=payload.getlist('appid')
    #appid=appid[0]
    macmobj=MACM.objects.filter(appId=appid)
    application=macmobj[0].application

    if(request.method=='POST'):


        response = HttpResponse(open("./macms/"+application+appid+".macm", 'rb').read())
        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename='+application+'_'+x+'.macm'
        return response


    return render(request, 'app/settings.html',{
        'appid':appid,
    })

    #return render(request, 'app/settings.html',{
    #    'appid':appid
    #})

def pass_to_pipeline(request):
    return render(request,'app/pipeline.html',request.GET)

def generate_pipeline(request):

    payload=request.POST
    #appid=payload.getlist('appid')
    #appid=appid[0]
    #print(payload)



    list=["\'","[","]","\'"]
    a=payload['application']
    application="".join(i for i in a if i not in list)
    application=re.sub('["]','',application)

    #l'app id mi serve come chiave per ottenere valori dal DB
    b=payload['appid']
    appid="".join(i for i in b if i not in list)
    appid=re.sub('["]','',appid)


    obj=MACM.objects.get(appId=appid)
    components=obj.components
    dev_type=obj.dev_types
    secondaries=obj.secondaries

    list2=["'",",","[","]"]
    components="".join(i for i in components if i not in list2)
    components=components.split()

    dev_type="".join(i for i in dev_type if i not in list2)
    dev_type=dev_type.split()

    secondaries="".join(i for i in secondaries if i not in list2)
    secondaries=secondaries.split()

    if request.method=='POST':

        username= payload['username']
        docker_hub = payload['docker_hub']
        password = payload['password']
        inspec = payload['inspec']
        button=payload['submit']

        print(request.POST)

        if username=="":
            error6="Campo 'Username' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error6':error6
        })


        if docker_hub=="":
            error7="Campo 'Docker Hub' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error7':error7
        })

        if password=="":
            error9="Campo 'Password' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error9':error9
        })

        if inspec=="":
            error10="Campo 'Inspec Id' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error10':error10
        })

        shutil.rmtree("app/pipeline")
        ind=0
        ind2=1
        for i in range(0,len(components),1):
            if secondaries[ind]=="SaaS":
                path="app/pipeline/pipeline_"+str(ind2)
                os.makedirs(path)
                file_pipeline=open("app/pipeline/pipeline_"+str(ind2)+"/Jenkinsfile","w")
                file_pipeline.write("pipeline {\nenvironment {\nregistry = '"+username+"/"+application+"/"+components[ind]+"'\n"
                                    "registryCredential = '"+docker_hub+"'\n"
                                    "dockerImage = ''\n"
                                    "DOCKER_TAG = getVersion().trim()\n"
                                    "IMAGE = '"+application+"'\n}"
                                    "\n\n"
            
                                    "agent any\n stages { \n\n")
                if dev_type[ind]=="custom":
                    file_pipeline=open("app/pipeline/pipeline_"+str(ind2)+"/Jenkinsfile","a")
                    file_pipeline.write(
                                        " stage('SonarQube analysis'){\n"
                                        "  steps{\n"
                                        "   sh 'echo SonarQube analysis'\n"
                                        " withSonarQubeEnv('Sonarqube') { \n"
                                        "  sh " 
                                        "\"${tool('Sonarqube')}/bin/sonar-scanner\""
                                        "\n}}}\n"
                                        "\n\n")

                    file_sonarqube=open("app/pipeline/pipeline_"+str(ind2)+"/sonar-project.properties","a")
                    file_sonarqube.write("sonar.projectKey="+application+"_application\n"
                                        "sonar.exclusions=**/*.java\n"
                                        "sonar.sources=./"+components[ind])

                file_pipeline=open("app/pipeline/pipeline_"+str(ind2)+"/Jenkinsfile","a")
                file_pipeline.write(
                                    " stage('Building image') {\n"
                                    "  steps{\n"
                                    "   sh 'echo Building Image'\n"
                                    "   script {\n"
                                    "     dockerImage = docker.build('$registry:$DOCKER_TAG')\n}}}\n"
                                    "\n\n"
                                                    
                                    " stage('Static Security Assesment'){\n"
                                    "  steps{\n"
                                    "   sh 'echo Static Security Assesment'\n"
                                    "   sh 'docker run --name ${IMAGE} -t -d $registry:${DOCKER_TAG}'\n"
                                    " withCredentials([usernamePassword(credentialsId: '"+inspec+"', passwordVariable: '"+password+"', usernameVariable: '"+inspec+"')]) {\n"
                                    " //inserire qui gli stig da definire in basde al tipo di sistema. Inseriamo 2 stig di esempio\n"
                                    " sh 'inspec exec https://github.com/dev-sec/linux-baseline -t docker://${IMAGE} --reporter html:Results/Linux_report.html --chef-license=accept || true'\n"
                                    " sh 'inspec exec https://github.com/dev-sec/apache-baseline -t docker://${IMAGE} --reporter html:Results/Apache_report.html --chef-license=accept || true'\n"
                                    " sh 'docker stop ${IMAGE}'\n"
                                    " sh 'docker container rm ${IMAGE}'\n}}}"
                                    "\n\n"
                            
                                    " stage('Push Image') {\n"
                                    "  steps{\n"
                                    "   sh 'echo Push Image'\n"
                                    "   script {\n"
                                    "    docker.withRegistry( '', registryCredential ) {\n"
                                    "      dockerImage.push()\n }}}}}}\n"
                            
                                    "def getVersion(){\n"
                                    " def commitHash = sh returnStdout: true, script: 'git rev-parse --short HEAD'\n"
                                    " return commitHash\n}"
                                    )

                ind2+=1
            ind+=1

        file_pipeline.close()


    return render(request, 'app/pipeline.html',
                  {'button':button})





#def viewmacm(request):
#    content = open("./"+request.POST['application_name']+".macm").read()
#    return HttpResponse(content, content_type='text/plain')
