import os

import pexpect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from . import dockercompose_to_macmFile
from neo4j import GraphDatabase
import datetime
from .models import *
import re
import shutil
import jenkins
from pexpect import pxssh
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
            print(payload)
            alist=[]
            for i in range(0,len(nodes),1):
                alist.append("")
            lista=zip(nodes,alist,alist,alist,alist,alist)
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
            #clist=obj_backup.custom_types
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
            ##ctype_backup="".join(i for i in clist if i not in list)
            components_backup="".join(i for i in components if i not in list)
            primaries_backup="".join(i for i in primaries if i not in list)
            secondaries_backup="".join(i for i in secondaries if i not in list)
            #ctype_backup=" ".join(i for i in ctype_backup if i not in list)
            #print(atype_backup.split())
            alist=atype_backup.split()
            dlist=dtype_backup.split()
            ##clist=ctype_backup.split()
            components=components_backup.split()
            primaries=primaries_backup.split()
            secondaries=secondaries_backup.split()
            obj_backup.delete()
            lista=zip(alist,alist,dlist,components,primaries,secondaries)
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
        #ctype=payload.getlist('custom_type')

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


        MACMobj_customize=MACM(appId=appid,application=application,components=components,primaries=primaries,secondaries=secondaries,asset_types=atype, dev_types=dtype)
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
        workspace=payload['workspace']
        jenkins_token=payload['jenkins_token']
        project_path=payload['project_path']
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

        if workspace=="":
            error15="Campo 'Workspace path Jenkins' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error15':error15
        })

        if jenkins_token=="":
            error16="Campo 'Jenkins Token' non valido.Riprova"
            return render(request, 'app/pipeline.html',{
            'error16':error16
        })


        list_fileconfigpath = []
        list_SaaS = []
        ind=0
        ind2=1
        for i in range(0,len(components),1):
            if secondaries[ind]=="SaaS":
                workspacePath=workspace+"/"+application+"_"+components[ind]
                list_SaaS.append(components[ind])
                fileconfigpath=workspacePath+"/config.xml"
                list_fileconfigpath.append(fileconfigpath)
                filesonarqubepath=workspacePath+"/sonar-project.properties"
                dockerfilepath=workspacePath+"/Dockerfile"
                #REMEMBER: scrivi docker file e poi aggiungi tag xml
                if os.path.exists(workspacePath):
                    shutil.rmtree(workspacePath)
                os.makedirs(workspacePath)

                fp=open(fileconfigpath,"w")
                fp.write(
                    "<?xml version='1.1' encoding='UTF-8'?>\n"
                    "<flow-definition plugin=\"workflow-job@2.42\">\n"
                    "<actions>\n\n"
                    "<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin=\"pipeline-model-definition@1.9.3\"/>\n"
                    "<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin=\"pipeline-model-definition@1.9.3\">\n"
                    "<jobProperties/>\n<triggers/>\n<parameters/>\n<options/>\n"
                    "</org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>\n"
                    "</actions>\n<description></description>\n"
                    "<keepDependencies>false</keepDependencies>\n"
                    "<properties/>\n"
                    "<definition class=\"org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition\" plugin=\"workflow-cps@2633.v6baeedc13805\">\n"
                    "<script>\n\n"
                )
                ##fp.write("prova9")
                #path=workspace+"/"+application+"_"+components[ind]+"_"+appid
                #os.makedirs(path)
                #riparti da qui sostituendo jenkinsfile con config.xml
                #crea quindi i vari casi e crea anche nell workspace dockerfile e eventuale sonarproperties
                #file_pipeline=open(path+"/Jenkinsfile","w")

                fp = open(fileconfigpath,"a")
                fp.write("pipeline {\nenvironment {\nregistry = '"+username+"/"+application+"'\n"
                                    "registryCredential = '"+docker_hub+"'\n"
                                    "dockerImage = ''\n"
                                    "DOCKER_TAG = '"+components[ind]+"'\n"
                                    "IMAGE = '"+application+"_"+str(ind)+"_"+appid+"'\n}"
                                    "\n\n"
            
            
                                    "agent any\n stages { \n\n")
                if dev_type[ind]=="custom":
                    dest=workspacePath+"/"+components[ind]+"-sonar"
                    src=project_path+"/"+components[ind]
                    os.makedirs(dest)
                    src_file=os.listdir(src)
                    for file_name in src_file:
                        full_file_name= os.path.join(src,file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name,dest)
                    src_file2=os.listdir(workspacePath)
                    for file_name2 in src_file2:
                        os.chmod(workspacePath+"/"+file_name2,0o777)
                    fp=open(fileconfigpath,"a")
                    fp.write(
                                        " stage('SonarQube analysis'){\n"
                                        "  steps{\n"
                                        "   sh 'echo SonarQube analysis'\n"
                                        " withSonarQubeEnv('Sonarqube') { \n"
                                        "  sh " 
                                        "\"${tool('Sonarqube')}/bin/sonar-scanner\""
                                        "\n}}}\n"
                                        "\n\n")

                    file_sonarqube=open(filesonarqubepath,"w")
                    file_sonarqube.write("sonar.projectKey="+application+"_"+components[ind]+"\n"
                                        "sonar.exclusions=**/*.java\n"
                                        "sonar.sources=./"+components[ind]+"-sonar\n")
                    file_sonarqube.close()
                fp=open(fileconfigpath,"a")
                fp.write(
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
                                    " sh 'inspec exec https://github.com/dev-sec/linux-baseline -t docker://${IMAGE} --reporter html:"+project_path+"/Results/"+components[ind]+"_Linux_report.html --chef-license=accept || true'\n"
                                    " sh 'inspec exec https://github.com/dev-sec/apache-baseline -t docker://${IMAGE} --reporter html:"+project_path+"/Results/"+components[ind]+"_Apache_report.html --chef-license=accept || true'\n"
                                    " sh 'docker stop ${IMAGE}'\n"
                                    " sh 'docker container rm ${IMAGE}'\n}}}"
                                    "\n\n"
                                    
                                    " stage('Push Image') {\n"
                                    "  steps{\n"
                                    "   sh 'echo Push Image'\n"
                                    "   script {\n"
                                    "    docker.withRegistry( '', registryCredential ) {\n"
                                    "     dockerImage.push()\n}}}}"
                                    "}}"
                                    )

                fp=open(fileconfigpath,"a")
                fp.write(
                    "\n</script>\n"
                    "<sandbox>true</sandbox>\n"
                    "</definition>\n"
                    "<triggers/>\n"
                    "<authToken>"+jenkins_token+"</authToken>\n"
                    "<disabled>false</disabled>\n"
                    "</flow-definition>"
                )

                fp_dockerfile=open(dockerfilepath,"w")
                fp_dockerfile.write(
                    "FROM node:latest\n"
                    "WORKDIR /usr/src/app\n"
                    "COPY . .\n"
                    "EXPOSE 3000\n"
                    "CMD [ \"node\" ]"
                )
                fp_dockerfile.close()

                ind2+=1
            ind+=1

        fp.close()


    return render(request, 'app/pipeline.html',
                  {'button':button,
                  'list_fileconfigpath':list_fileconfigpath,
                   'list_SaaS':list_SaaS,
                   'application':application
                   })


def send_pipeline(request):
    payload=request.POST
    JENKINS_URL = "http://localhost:8080/"
    JENKINS_USERNAME = payload['jenkins_username']
    JENKINS_PASSWORD = payload['jenkins_password']
    JENKINS_SHEET = payload['jenkins_sheet']

    list2=["'",",","[","]"]

    list_SaaS=payload.getlist('list_SaaS')
    list_SaaS=list_SaaS[0]
    list_SaaS="".join(i for i in list_SaaS if i not in list2)
    list_SaaS=list_SaaS.split()

    list_fileconfigpath=payload.getlist('list_fileconfigpath')
    list_fileconfigpath=list_fileconfigpath[0]
    list_fileconfigpath="".join(i for i in list_fileconfigpath if i not in list2)
    list_fileconfigpath=list_fileconfigpath.split()

    list=["\'","[","]","\'"]
    a=payload['application']
    application="".join(i for i in a if i not in list)
    application=re.sub('["]','',application)

    #a partire da listSaaS e listfileconfigpath provasre a invaire le varie pipeline
    #gestisci comparizione e scomparizione jenkins username e jenkins password prima e dopo il post
    #nell' if post che segue tutto deve essere tolto il commento
    if request.method=='POST':

        #try:
        #    payload['submit2']
        #except NameError:
        #    var_exists = False
        #else:
        #    button_sendpipeline=application+"_"+payload['submit2']
        #    var_exists = True
        button_sendpipeline=JENKINS_SHEET+"_"+payload['submit2']
        #button_sendcredential=payload['submit3']

        #print("YAAAAAAAAAA")
        #print(payload)
        #print(button_sendpipeline)
        #print(list_SaaS)
        #print(list_fileconfigpath)
        if payload['submit2']!="Go To Deploy":

            if JENKINS_USERNAME=="":
                error20="Campo 'Jenkins Username' non valido.Riprova"
                return render(request, 'app/pipeline.html',{
                'error20':error20,
                'list_SaaS':list_SaaS,
                'list_fileconfigpath':list_fileconfigpath,
                'button_sendpipeline':button_sendpipeline
            })

            if JENKINS_PASSWORD=="":
                error21="Campo 'Jenkins Password' non valido.Riprova"
                return render(request, 'app/pipeline.html',{
                'error21':error21,
                'list_SaaS':list_SaaS,
                'list_fileconfigpath':list_fileconfigpath,
                'button_sendpipeline':button_sendpipeline
            })

            if JENKINS_SHEET=="":
                error22="Campo 'Jenkins Sheet' non valido.Riprova"
                return render(request, 'app/pipeline.html',{
                'error22':error22,
                'list_SaaS':list_SaaS,
                'list_fileconfigpath':list_fileconfigpath,
                'button_sendpipeline':button_sendpipeline
            })

            jenkins_server = jenkins.Jenkins(JENKINS_URL,
                                             username=JENKINS_USERNAME,
                                             password=JENKINS_PASSWORD)
            jobs = jenkins_server.get_jobs()

        #jobs_name = []
        #for i in range(0,len(jobs),1):
        #    for key in jobs[i].items():
        #        if key[0]=='name':
        #            jobs_name.append(key[1])


        #for name in jobs_name:
        #    if name==button_sendpipeline:
        #    #if name==button_sendpipeline:
        #        jenkins_server.delete_job(name)


        if payload['submit2']!="Send All Pipeline" and payload['submit2']!="Go To Deploy":

            jobs_name = []
            for i in range(0,len(jobs),1):
                for key in jobs[i].items():
                    if key[0]=='name':
                        jobs_name.append(key[1])


            for name in jobs_name:
                if name==button_sendpipeline:
                #if name==button_sendpipeline:
                    jenkins_server.delete_job(name)

            temp_fileconfigPath = None
            for i in range(0,len(list_SaaS),1):
                if JENKINS_SHEET+"_"+list_SaaS[i]==button_sendpipeline:
                    temp_fileconfigPath=list_fileconfigpath[i]

            if temp_fileconfigPath!=None:
                fp= open(temp_fileconfigPath,"r")
                config=fp.read()
                fp.close()






                jenkins_server.create_job(button_sendpipeline,config)
                jenkins_server.build_job(button_sendpipeline)
        #jenkins_server.create_job(button_sendpipeline,config)
        #jenkins_server.build_job(button_sendpipeline)

        if payload['submit2']=="Send All Pipeline":
            jobs_name = []
            for i in range(0,len(jobs),1):
                for key in jobs[i].items():
                    if key[0]=='name':
                        jobs_name.append(key[1])

            for i in range(0,len(list_SaaS),1):
                name=JENKINS_SHEET+"_"+list_SaaS[i]
                try:
                    jenkins_server.delete_job(name)
                except:
                    print("")

            #i=0
            #for name in jobs_name:
             #   print(name)
             #   if name==application+"_"+list_SaaS[i]:
                #if name==button_sendpipeline:
              #      jenkins_server.delete_job(name)
            #i=i+1

            for i in range(0,len(list_SaaS),1):
                if list_fileconfigpath[i]!=None:
                    fp= open(list_fileconfigpath[i],"r")
                    config=fp.read()
                    fp.close()
                    jenkins_server.create_job(JENKINS_SHEET+"_"+list_SaaS[i],config)
                    jenkins_server.build_job(JENKINS_SHEET+"_"+list_SaaS[i])

        if payload['submit2']=="Go To Deploy":
            return render(request, 'app/deploy.html')

    return render(request, 'app/pipeline.html',
                  {'button_sendpipeline':button_sendpipeline,
                   'list_SaaS':list_SaaS,
                   'list_fileconfigpath':list_fileconfigpath
                   #'button_sendcredential':button_sendcredential
                   })


def deploy(request):
    payload= request.POST
    DEPLOY_IP=payload['remote_ip']
    DEPLOY_USER=payload['remote_username']
    DEPLOY_PASSWORD=payload['remote_password']
    DEPLOY_COMMAND=payload['remote_command']

    if request.method=='POST':



        if DEPLOY_IP=="":
            error30="Campo 'IP' non valido.Riprova"
            return render(request, 'app/deploy.html',{
            'error30':error30
        })

        if DEPLOY_USER=="":
            error31="Campo 'USER' non valido.Riprova"
            return render(request, 'app/deploy.html',{
            'error31':error31
        })

        if DEPLOY_PASSWORD=="":
            error32="Campo 'PASSWORD' non valido.Riprova"
            return render(request, 'app/deploy.html',{
            'error32':error32
        })

        s = pxssh.pxssh(timeout=1000)
        if not s.login (DEPLOY_IP, DEPLOY_USER, DEPLOY_PASSWORD):
            print("SSH session failed on login.")
            print(str(s))
        else:
            print("SSH session login successful")
            s.sendline(DEPLOY_COMMAND) #più comandi possono essere divisi da ;
            s.prompt()         # match the prompt
            print("AAAAAAAAA")
            print(s.before)     # print everything before the prompt.
            s.logout()

    return render(request, 'app/deploy.html')

#def viewmacm(request):
#    content = open("./"+request.POST['application_name']+".macm").read()
#    return HttpResponse(content, content_type='text/plain')
#end
