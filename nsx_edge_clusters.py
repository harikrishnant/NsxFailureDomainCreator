'''This module applies Failure Domain allocation policy to Edge Cluster '''
__version__ = 1.0
__author__ = "Harikrishnan T"
__website__ = "vxplanet.com"

import requests
from tabulate import tabulate

class NsxEdgeCluster:
    def __init__(self,url,headers,cookies):
        self._url = url
        self._headers = headers
        self._cookies = cookies

    def get_edge_cluster(self):
        '''This method gets the detail of edge cluster available in NSX'''
        self._list_edge_clusters = []
        self._dict_ec_id_name = {}
        self._list_tabulate_ec = []
        response = requests.get(self._url + "/api/v1/edge-clusters", headers=self._headers, cookies=self._cookies, verify=False)
        list_response_results = response.json().get("results", [])
        if response and list_response_results:
            for ec in list_response_results:
                self._list_edge_clusters.append(ec)
                self._dict_ec_id_name.update({
                    ec.get("id") : ec.get("display_name")
                })
                ec_edge_nodes = "\n".join([member.get("display_name", "NONE") for member in ec.get("members", {})])
                #print([rule.get("action").get("action_type") for rule in ec.get("allocation_rules", [{"action": {"action_type":"None"}}])])
                if ec.get("allocation_rules", []) == []:
                    fd_allocation_policy = "None"
                else:
                    fd_allocation_policy = [rule.get("action").get("action_type") for rule in ec.get("allocation_rules")]
                self._list_tabulate_ec.append([ec.get("display_name"), ec.get("id"), ec_edge_nodes if ec_edge_nodes else "None", fd_allocation_policy])
        else:
            print(f"\nNOT FOUND!!! No Edge Clusters found ({response.status_code})\n")
        if self._list_tabulate_ec:
            print("\nThe below Edge Clusters are available\n")
            print(tabulate(self._list_tabulate_ec, headers=["Edge Cluster", "ID", "Edge Nodes", "FD Allocation"], showindex=True, tablefmt="fancy_grid"))

    def update_edge_cluster(self):
        '''This method updates the edge cluster with FD Allocation policy'''
        self.get_edge_cluster()
        ec_choice = input("\nEnter the Edge Cluster name to receive Failure Domain Allocation Policies: ")
        if ec_choice in self._dict_ec_id_name.values():
            for ec_item in self._list_edge_clusters:
                if ec_choice == ec_item.get("display_name"):
                    ec_item["allocation_rules"] = [
                            {
                                "action" : {
                                    "enabled" : "true",
                                    "action_type" : "AllocationBasedOnFailureDomain"
                                }
                            }
                        ]
                    response = requests.put(self._url + "/api/v1/edge-clusters/" + ec_item.get("id"), headers=self._headers, cookies=self._cookies, json=ec_item, verify=False)
                    if response:
                        print(f"\nSUCCESS!!! Failure domain allocation policies have been successfully mapped to {ec_choice} - ({response.status_code})\n")
                    else:
                        print(f"\nFAILURE!!! Failure domain allocation policies mapping failed ({response.status_code})\n")
                        print(response.json())
        else:
            print("\nNOT FOUND!!! Selected edge cluster not found. Please try again!")
    
    def remove_edge_fd_allocation(self):
        ''' This method disassociates edge cluster fro mthe FD allocation policy'''
        self.get_edge_cluster()
        choice_ec_unmap = input("\nEnter Edge Cluster to remove FD allocation: ")
        if choice_ec_unmap in self._dict_ec_id_name.values():
            for edge_cluster in self._list_edge_clusters:
                if choice_ec_unmap == edge_cluster.get("display_name"):
                    edge_cluster["allocation_rules"] = []
                    response = requests.put(self._url + "/api/v1/edge-clusters/" + edge_cluster.get("id"), headers=self._headers, cookies=self._cookies, json=edge_cluster, verify=False)
                    if response:
                        print(f"\nSUCCESS!!! Failure domain allocation policies have been successfully removed from {choice_ec_unmap} - ({response.status_code})\n")
                    else:
                        print(f"\nFAILURE!!! Failure domain allocation policies removal from {choice_ec_unmap} failed ({response.status_code})\n")
                        print(response.json())
        else:
            print(f"\nNOT FOUND!!! Selected Edge Cluster {choice_ec_unmap} not found\n")
        self.get_edge_cluster()