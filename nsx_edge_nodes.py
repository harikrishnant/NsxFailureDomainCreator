'''This module applies Failure Domains to Edge Nodes '''
__version__ = 1.0
__author__ = "Harikrishnan T"
__website__ = "vxplanet.com"

import requests
from tabulate import tabulate

class NsxEdgeNode:
    def __init__(self,url,headers,cookies):
        self._url = url
        self._headers = headers
        self._cookies = cookies

    def get_edge_node(self):
        '''Method to get the list of edge transport nodes'''
        response = requests.get(self._url + "/api/v1/transport-nodes", headers=self._headers, cookies=self._cookies, verify=False)
        list_response_results = response.json().get("results", [])
        self._list_all_edge_nodes = []
        self._list_tabulate_edge_nodes = []
        self._dict_edge_node_id_name = {}
        if response and list_response_results:
            for tn in list_response_results:
                failure_domain_id = "NONE"
                if tn.get("node_deployment_info", {}).get("resource_type", "") == "EdgeNode":
                    ec_name = "NONE"
                    response_ec = requests.get(self._url + "/api/v1/edge-clusters", headers=self._headers, cookies=self._cookies, verify=False)
                    list_response_ec_results = response_ec.json().get("results", [])
                    if response_ec and list_response_ec_results:
                        for ec in list_response_ec_results:
                            for member in ec.get("members", {}):
                                if member.get("transport_node_id", "") == tn.get("id"):
                                    ec_name = ec.get("display_name")
                    self._list_all_edge_nodes.append(tn)
                    self._dict_edge_node_id_name.update({
                        tn.get("id"): tn.get("display_name")                      
                    })
                    response_tn = requests.get(self._url + "/api/v1/transport-nodes/" + tn.get("id"), headers=self._headers, cookies=self._cookies, verify=False) #Only calling api this way retrieves edge FD info
                    failure_domain_id = response_tn.json().get("failure_domain_id", "NONE")
                    response_fd = requests.get(self._url + "/api/v1/failure-domains", headers=self._headers, cookies=self._cookies, verify=False)
                    response_fd_body = response_fd.json().get("results", [])
                    for each in response_fd_body:
                        if failure_domain_id == each.get("id"):
                            failure_domain_name = each.get("display_name", "NONE")
                    self._list_tabulate_edge_nodes.append([tn.get("display_name"), tn.get("id"), ec_name, failure_domain_name])                    
        else:
            print(f"\nNo NSX Edge Transport Nodes found ({response.status_code})\n")
            print(response.json())
        if self._list_tabulate_edge_nodes:
            print("\nThe below NSX Edge Transport Nodes are available\n")
            print(tabulate(self._list_tabulate_edge_nodes, headers=["Edge Node", "ID", "Edge Cluster", "Failure Domain"], showindex=True, tablefmt="fancy_grid"))

    def update_edge_node(self, dict_fd_id_name):
        ''' This method maps edge nodes to selected edge failure domains '''
        fd_choice = input("\nEnter Failure Domain to be associated to edge nodes: ")
        if fd_choice in dict_fd_id_name.values():
            for id,name in dict_fd_id_name.items():
                if fd_choice == name:
                    fd_id = id
            self.get_edge_node()
            edge_choice = input("\nSelect Edge Transport Node(s) to be associated to selected Failure Domain (Eg:edge1,edge2): ").split(",")
            for edge in edge_choice:
                if edge in self._dict_edge_node_id_name.values():
                    for edge_tn in self._list_all_edge_nodes:
                        if edge == edge_tn.get("display_name"):
                            edge_tn["failure_domain_id"] = fd_id
                            response = requests.put(self._url + "/api/v1/transport-nodes/" + edge_tn.get("id"), headers=self._headers, cookies=self._cookies, json=edge_tn, verify=False)
                            if response:
                                print(f"\nSUCCESS!!! Edge Failure Domain {fd_choice} successfully mapped to {edge} - ({response.status_code})\n")
                            else:
                                print(f"FAILURE!!! Edge Failure Domain mapping failed ({response.status_code})")
                                print(response.json())
                else:
                    print(f"\nNOT FOUND!!! Selected Edge node {edge} not found\n")
        else:
            print(f"\nNOT FOUND!!! Selected Failure Domain {fd_choice} not found\n")
        self.get_edge_node()

    def unmap_edge_node(self, dict_fd_id_name):
        ''' This method unmaps edge node from the failure domain '''
        for fd_id, fd_name in dict_fd_id_name.items():
            if fd_name == "system-default-failure-domain":
                default_fd = fd_id
        self.get_edge_node()
        choice_edge_unmap = input("\nEnter Edge Node(s) to unmap the failure domains from (Eg: edge1,edge2): ").split(",")
        for each_choice in choice_edge_unmap:
            if each_choice in self._dict_edge_node_id_name.values():
                for edge_node in self._list_all_edge_nodes:
                    if each_choice == edge_node.get("display_name"):
                        edge_node["failure_domain_id"] = default_fd
                        response = requests.put(self._url + "/api/v1/transport-nodes/" + edge_node.get("id"), headers=self._headers, cookies=self._cookies, json=edge_node, verify=False)
                        if response:
                            print(f"\nSUCCESS!!! Edge Failure Domain successfully unmapped from {each_choice} - ({response.status_code})\n")
                        else:
                            print(f"\nFAILURE!!! Edge Failure Domain unmapping failed ({response.status_code})")
                            print(response.json())
            else:
                print(f"\nNOT FOUND!!! Selected Edge node {each_choice} not found\n")
        self.get_edge_node()