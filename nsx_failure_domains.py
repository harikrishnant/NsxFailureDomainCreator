'''This module creates an Edge failure domain object '''
__version__ = 1.0
__author__ = "Harikrishnan T"
__website__ = "vxplanet.com"

import requests
from tabulate import tabulate
import sys

class NsxFailureDomain:
    def __init__(self, url, headers, cookies):
        self._url = url
        self._headers = headers
        self._cookies = cookies

    def get_failure_domain(self):
        ''' This method returns the list of failure domains that are available '''
        self.list_df_fd = []
        response = requests.get(self._url + "/api/v1/failure-domains", headers=self._headers, cookies=self._cookies, verify=False)
        list_response_results = response.json().get("results", [])
        if response and list_response_results:
            self.dict_fd_id_name = {item.get("id"):item.get("display_name") for item in list_response_results}
            for item in list_response_results:
                self.list_df_fd.append([item.get("display_name"), item.get("id"), item.get("preferred_active_edge_services", "True")])
            print("\nThe below NSX Edge Failure Domains are available:\n")
            print(tabulate(list(self.list_df_fd), headers=["Display Name", "ID", "Preferred Active"], showindex=True, tablefmt="fancy_grid"))
        else:
            print("\nERROR!!! NSX Edge Failure Domains not found\n")
            print(response.json())

    def create_failure_domain(self):
        ''' This method creates edge failure domains based on user input '''
        fd_modes = ["Preferred Active", "Preferred Standby"]
        input_fd_mode = input(f"\nEnter Failure Domain mode - 'A' for {fd_modes[0]} and 'S' for {fd_modes[1]}: ").upper()
        input_fd_name = input("\nEnter name for Edge Failure domain: ")
        fd_body = {
            "display_name": input_fd_name,
            "preferred_active_edge_services": "false" if input_fd_mode == "S" else "true" if input_fd_mode == "A" else sys.exit("\nInvalid FD Mode selected. Choose Active(A) or Standby(S)")
        }
        response = requests.post(self._url + "/api/v1/failure-domains", headers=self._headers, cookies=self._cookies, json=fd_body, verify=False)
        if response:
            print(f"\nSUCCESS!!! Edge Failure Domain Creation Succeeded ({response.status_code})")
            #print(tabulate([[response.json().get("display_name"), response.json().get("id"), response.json().get("preferred_active_edge_services")]], headers=["Failure Domain", "ID", "Preferred Active"], showindex=True, tablefmt="fancy_grid"))
        else:
            print(f"\nFAILED!!! Edge Failure Domain creation failed ({response.status_code})")
            print(response.json())
        self.get_failure_domain()

    def delete_failure_domain(self):
        ''' This method deletes the edge failure domains based on user input '''
        self.get_failure_domain()
        delete_fd_choice = input("\nSelect Edge Failure Domain(s) from the list above. (Eg: fd0,fd1): ").split(",")
        dict_deleted_fd_name_id = {}
        if delete_fd_choice != [""]:
            for each in delete_fd_choice:
                if each in self.dict_fd_id_name.values():
                    for fd_id, fd_name in self.dict_fd_id_name.items():
                        if each == fd_name:
                            response = requests.delete(self._url + "/api/v1/failure-domains/" + fd_id, headers=self._headers, cookies=self._cookies, verify=False)
                            if response:
                                print(f"\nSUCCESS!!! Edge Failure Domain {each} deleted successfully ({response.status_code})")
                                dict_deleted_fd_name_id.update({
                                    each: fd_id
                                })
                            else:
                                print(f"\nFAILURE!!! Edge Failure Domain {each} deletion failed ({response.status_code})")
                                print(response.json())
                else:
                    print(f"\nNOT FOUND!!! Edge Failure Domain {each} not found. Use Menu Option 1 to verify the Failure Domain name: ")
        else:
            print("\nNO SELECTION!!! No entries selected:")
        if dict_deleted_fd_name_id:
            print("\nThe below Edge Failure Domains are deleted successfully:\n")
            print(tabulate(list(map(list, dict_deleted_fd_name_id.items())), headers=["Failure Domain", "ID"], showindex=True, tablefmt="fancy_grid"))