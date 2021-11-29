import networkx as nx
import re
from networkx import *
import yaml
import os
import sqlite3


class Node(DiGraph):
	def __init__(self, label, namee, type_node):
		self.label=label
		self.namee=namee
		self.type_node=type_node
		
	def get_label(self):
		return self.label
	
	def get_name(self):
		return self.namee
	
	def get_type(self):
		return self.type_node

		

class Edge(DiGraph):
	def __init__(self, by_node , to_node, type_connect):
		self.by_node=by_node
		self.to_node=to_node
		self.type_connect=type_connect
		
	def get_bynode(self):
		return self.by_node
	
	def get_tonode(self):
		return self.to_node
	
	def get_type_connect(self):
		return self.type_connect


def getnode_fromname(self,namee):
	if self.get_name()==namee:
		return self		


		
def filtering(x):
	return re.sub('[- ]','',x)


def dockercompose_WriteTo_macmFile(dockercompose_path, app_id, application_name):

	file_cypher=open(os.getcwd()+"/"+application_name+".macm","w")
	file_cypher.write("CREATE\n")

	#creo grafo
	macm=nx.DiGraph()

	object_node = []
	object_edge = []

	node_container = []
	node_networks = []
	edge_uses = []
	edge_connects = []
	edge_connects_default_networks = []
	edge_hosts = []

	container_name = []

	networks = []
	networks_connects = []

	depends_on = []

	ports = []
	ports_container = []

	fp=open(dockercompose_path,"r")
	fp2=fp.read()



	#converto yml in dizionario:
	docker_composeObj=(yaml.safe_load(fp2))



	#ottengo i container name
	for key,value in docker_composeObj['services'].items():
		container_name.append(key)



	#NETWORKS: ottengo le networks associate ai singoli container per le relazioni di uses
	ind=0
	for x in container_name:
		for key,value in docker_composeObj['services'][x].items():
			#definiamo l'if siccome networks può non essere presente nel docker compose
			if(key=='networks'):
				ind+=1
				networks_connects.append(docker_composeObj['services'][x]['networks'])
	if ind==0:
		print("Non è presente alcuna 'networks' nel docker compose\n")



	#NETWORKS: ottengo le networks(uno per tipo non replicato) per la creazione di nodi networks(se presenti)
	if(len(networks_connects)!=0):
		for key in docker_composeObj['networks'].keys():
			networks.append(key)



	#DEPENDS_ON: ottengo le depends_on associate ai singoli container per le relazioni di connects
	ind=0
	for x in container_name:
		for key,value in docker_composeObj['services'][x].items():
			#definiamo l'if siccome depends_on può non essere presente nel docker compose
			if(key=='depends_on'):
				ind+=1
				depends_on.append(docker_composeObj['services'][x]['depends_on'])
	if ind==0:
		print("Non è presente nessuna 'depends_on' nel docker compose\n")



	#uso sqlite3 per accedere al DB creato per una gestione più accurata dei porti noti
	con = sqlite3.connect('portDB.db')
	cur = con.cursor()

	numb_port_asset = []
	asset_type_DB = []
	numb_port_protocol = []
	protocol_DB = []
	for row in cur.execute('SELECT numb_port,asset_type FROM port WHERE asset_type!=""'):
		numb_port_asset.append(str(row[0]))
		asset_type_DB.append(str(row[1]))
	for row in cur.execute('SELECT numb_port,protocol FROM port WHERE protocol!=""'):
		numb_port_protocol.append(str(row[0]))
		protocol_DB.append(str(row[1]))

	con.close()

	#ottieni ports container e associa asset type e protocol
	ind00=0
	net00 = []
	properties0 = []
	for x in container_name:
		properties0.append(list(docker_composeObj['services'][x].keys()))

	for j in range(0,len(container_name),1):
		ind00=0
		for i in range(0,len(properties0[j]),1):
			if(properties0[j][i]=='ports'):
				net00.insert(j,1)
			if(properties0[j][i]!='ports'):
				ind00+=1
			if(ind00==len(properties0[j])):
				net00.insert(j,0)

	ind01=0
	for x in container_name:
		for key,value in docker_composeObj['services'][x].items():
			#definiamo l'if siccome depends_on può non essere presente nel docker compose
			if(key=='ports'):
				ind01+=1
				ports.append(docker_composeObj['services'][x]['ports'])
	if(ind01==0):
		print("Non è presente alcun 'ports' nel docker compose")

	if(ind01!=0): #mi assicuro che esistano ports
		net3 = [] #verifico quanti numeri di porti associati ai container ci sono
		temp = ""
		for j in range(0,len(ports),1):
			net3.insert(j,len(ports[j]))
			for k in range(0,len(ports[j]),1):
				flag=0
				for i in range(0,len(ports[j][k]),1):
					a=1
					if(flag==1):
						temp=temp+ports[j][k][i]
					if(ports[j][k][i]==':'):
						flag=1

				ports_container.append(temp)
				temp = ""

	for j in range(0,len(net00),1):
		#nei container che non è presente la chiave ports inserire '?' per trasferirlo poi all'asset type
		if(net00[j]==0):
			ports_container.insert(j,'?')

	if(ind01!=0):
		#definisco gli asset_type secondo i porti noti
		asset_type = []
		for x in range(0,len(container_name),1):
			flag2=0
			for y in range(0,net00[x],1):
				for j in range(0,len(numb_port_asset),1):
					if(ports_container[x]==numb_port_asset[j] and flag2==0):
						asset_type.append(asset_type_DB[j])
						flag2=1

			if(flag2==0):
				asset_type.append('?')

		#definisco i protocolli per i porti noti
		protocol_type = []
		for x in range(0,len(container_name),1):
			flag3=0
			for y in range(0,net00[x],1):
				for j in range(0,len(numb_port_protocol),1):
					if(ports_container[x]==numb_port_protocol[j] and flag3==0):
						protocol_type.append('{protocol:"'+protocol_DB[j]+'"}')
						flag3=1

			if(flag3==0):
				protocol_type.append('')


	#creo nodo VM che fa da host per tutti i container
	VM=Node("IaaS:service","VM1","VM")
	object_node.append(VM)
	macm.add_node(VM)
	Docker=Node("PaaS:service","Docker","?")
	object_node.append(Docker)
	macm.add_node(Docker)

	#se c'è qualche container privo di networks creo nodo default-network
	if(len(networks_connects) != len(container_name)):
		default_network=Node("network","default-network","?")
		object_node.append(default_network)
		macm.add_node(default_network)

	#creato i nodi container
	ind=0
	for x in container_name:
		node_container.append(Node("SaaS:service",x,asset_type[ind]))
		object_node.append(node_container[ind])
		macm.add_node(node_container[ind])
		ind+=1


	#creo i nodi networks(se presenti)
	if(len(networks_connects)!=0):
		ind=0
		for x in networks:
			node_networks.append(Node("network",x,"?"))
			object_node.append(node_networks[ind])
			macm.add_node(node_networks[ind])
			ind+=1


	#creo gli archi uses se le depends_on sono presenti nel docker compose
	if(len(depends_on)!=0):
		ind=0
		count=0
		count_edge=0
		for x in container_name:
			for key in docker_composeObj['services'][x].keys():
				#definiamo l'if siccome depends_on non è presente in tutti i container

				if(key=='depends_on'):
					#itero nella lista di liste
					for i in range(0,len(depends_on[ind]),1):

						#di seguito vado ad ottenere il to_node(nodo destinazione in cui punta l'arco) a partire dal nome del container del nodo destinazione
						ind2=0
						to_node = None
						while to_node == None:
							to_node=getnode_fromname(node_container[ind2],depends_on[ind][i])
							ind2+=1

						#il nodo da cui parte l'arco è sempre corretto grazie all'if che abbiamo inserito
						edge_uses.append(Edge(node_container[count],to_node,"uses"+protocol_type[count]))
						object_edge.append(edge_uses[count_edge])
						macm.add_edge(node_container[count],to_node,attribute="uses"+protocol_type[count])
						count_edge+=1

					ind+=1
			count+=1


	#creo gli archi connects per connettere alla default-network quando il container non ha una network associata
	properties = []
	ind=0
	net = []
	for x in container_name:
		properties.append(list(docker_composeObj['services'][x].keys()))


	for j in range(0,len(container_name),1):
		ind=0
		for i in range(0,len(properties[j]),1):
			if(properties[j][i]=='networks'):
				net.insert(j,1)
			if(properties[j][i]!='networks'):
				ind+=1
			if(ind==len(properties[j])):
				net.insert(j,0)

	count=0
	for j in range(0,len(net),1):
		if(net[j]==0):
			edge_connects_default_networks.append(Edge(node_container[j],default_network,"connects"))
			object_edge.append(edge_connects_default_networks[count])
			macm.add_edge(node_container[j],default_network,attribute="connects")
			count+=1


	#creo gli archi connects se le networks sono presenti nel docker compose
	#il valore q lo utilizziamo per non inserire la virgola nell'ultima connect
	if(len(networks_connects)!=0):
		ind=0
		count=0
		count_edge=0
		for x in container_name:
			for key in docker_composeObj['services'][x].keys():
				if(key=='networks'):
					#q=len(container_name)-1
					for i in range(0,len(networks_connects[ind]),1):
						ind2=0
						to_node = None
						while to_node == None:
							to_node=getnode_fromname(node_networks[ind2],networks_connects[ind][i])
							ind2+=1

						#il nodo da cui parte l'arco è corretto grazie all'if che abbiamo inserito
						edge_connects.append(Edge(node_container[count],to_node,"connects"))
						object_edge.append(edge_connects[count_edge])
						macm.add_edge(node_container[count],to_node,attribute="connects")
						count_edge+=1
					ind+=1
			count+=1




	#creo arco hosts da VM a Docker
	edge=Edge(VM,Docker,"hosts")
	object_edge.append(edge)
	macm.add_edge(VM,Docker,attribute="hosts")




	#creo gli archi hosts da VM per tutti i container
	count_edge=0
	for i in range(0,len(container_name),1):
		ind2=0
		to_node = None
		while to_node == None:
			to_node=getnode_fromname(node_container[ind2],container_name[i])
			ind2+=1

		edge_hosts.append(Edge(Docker,to_node,"hosts"))

		object_edge.append(edge_hosts[count_edge])
		macm.add_edge(Docker,to_node,attribute="hosts")
		count_edge+=1


	print("\n")



	#segnalo in output quali container non presentano le depends_on (nel caso in cui le presentano tutte non ha alcun effetto)
	ind=0
	net2 = []
	for x in container_name:
		properties.append(list(docker_composeObj['services'][x].keys()))


	for j in range(0,len(container_name),1):
		ind=0
		for i in range(0,len(properties[j]),1):
			if(properties[j][i]=='depends_on'):
				net2.insert(j,1)
			if(properties[j][i]!='depends_on'):
				ind+=1
			if(ind==len(properties[j])):
				net2.insert(j,0)

	for j in range(0,len(net2),1):
		if(net2[j]==0):
			print("Il container "+container_name[j]+" non presenta depends_on")

	#devtype
	dev_type = []
	for i in range(0,len(object_node),1):
		dev_type.append("?")

	#add node & edge to macmFile
	for i in range(0,len(object_node),1):
		file_cypher.write("\t("+filtering(object_node[i].get_name())+":"+object_node[i].get_label()+" {name:'"+object_node[i].get_name()+"', type:'"+object_node[i].get_type()+"', dev_type:'"+dev_type[i]+"', app_id:'"+app_id+"', application:'"+application_name+"'}),\n")
	file_cypher.write("\n")
	for i in range(0,len(object_edge),1):
		#if per la virgola finale da omettere nel macm
		if(i!=len(object_edge)-1):
			file_cypher.write("\t("+filtering(object_edge[i].get_bynode().get_name())+")-[:"+object_edge[i].get_type_connect()+"]->("+filtering(object_edge[i].get_tonode().get_name())+"),\n")
		if(i==len(object_edge)-1):
			file_cypher.write("\t("+filtering(object_edge[i].get_bynode().get_name())+")-[:"+object_edge[i].get_type_connect()+"]->("+filtering(object_edge[i].get_tonode().get_name())+")\n")

	#stampa dell'oggetto grafo finale
	print("\nL'oggetto grafo finale è il seguente:")
	print(macm)


	return macm


