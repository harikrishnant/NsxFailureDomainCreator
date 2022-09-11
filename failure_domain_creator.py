''' This is the main module to create edge failure domains, apply to edge nodes and set edge cluster allocation policies '''
#Import Modules
from nsx_login import NsxLogin
from nsx_failure_domains import NsxFailureDomain
from nsx_edge_nodes import NsxEdgeNode
from nsx_edge_clusters import NsxEdgeCluster
import urllib3
import sys
import argparse
from getpass import getpass
from tabulate import tabulate
import titles
import pyfiglet

#Parser Block
parser = argparse.ArgumentParser(description="NSX Edge Failure Domain Creator", epilog="Author : Harikrishnan T (@hari5611). Visit vxplanet.com for more information", add_help=True)
parser.add_argument("-v", "--version", action="version", version="NSX Edge Failure Domain Creator V1.0")
parser.add_argument("-u", "--username", action="store", type=str, metavar="USERNAME", dest="username", required=True, help="User with admin privileges to NSX")
parser.add_argument("-p", "--password", action="store", type=str, metavar="PASSWORD", dest="password", required=False, help="User Password")
parser.add_argument("-i", "--nsx_manager", action="store", type=str, metavar="NSX_MANAGER_IP/FQDN", dest="nsx_manager_ip", required=True, help="NSX Manager IP or FQDN")
args = parser.parse_args()

#Disable insecure certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Set API request header. Content Type "application/x-www-form-urlencoded" is required for login.
headers = {
    "Content-Type"  :   "application/x-www-form-urlencoded"
}

#Set NSX Manager FQDN and body for API POST
URL = "https://" + args.nsx_manager_ip

login = {
    "j_username"    :   args.username,
    "j_password"    :   args.password if args.password else getpass(prompt="\nEnter Password: ")
}

# Create NSX login session object
nsx_login = NsxLogin(URL, headers, login)
nsx_login.create_session()
headers.update({
    "X-XSRF-TOKEN"  :   nsx_login.xsrftoken
})
session_cookie = nsx_login.cookie
headers["Content-Type"] =  "application/json" #Content Type application/json required for subsequent operations

print(pyfiglet.figlet_format("NSX  Edge  Failure  Domain  Creator", width=180))

#Main recursive function
def run():    
    print("\n\n",titles.menu)

    choice = input("Choice: ")

    #initialize Objects
    nsx_failure_domain = NsxFailureDomain(URL, headers, session_cookie)
    nsx_edge_node = NsxEdgeNode(URL, headers, session_cookie)
    nsx_edge_cluster = NsxEdgeCluster(URL, headers, session_cookie)

    # Print Edge Failure Domains
    if choice == "1":  
        print("\n",pyfiglet.figlet_format("Print  Edge  Failure  Domains", width=180))      
        nsx_failure_domain.get_failure_domain()

    # Create Edge Failure Domain
    elif choice == "2":
        print("\n",pyfiglet.figlet_format("Create  Edge  Failure  Domain", width=180))
        nsx_failure_domain.create_failure_domain()
    
    # Delete Edge Failure Domain
    elif choice == "3":
        print("\n",pyfiglet.figlet_format("Delete  Edge  Failure  Domains", width=180))
        nsx_failure_domain.delete_failure_domain()

    # Get Edge Transport Nodes
    elif choice == "4":
        print("\n",pyfiglet.figlet_format("Print  Edge  Transport  Nodes", width=180))
        nsx_edge_node.get_edge_node()

    # Map Edge nodes to Failure Domains
    elif choice == "5":
        print("\n",pyfiglet.figlet_format("Edge  Node - FD  Mapping", width=180))
        nsx_failure_domain.get_failure_domain()
        nsx_edge_node.update_edge_node(nsx_failure_domain.dict_fd_id_name)

    #Unmap Edge Nodes from Failure Domain
    elif choice == "6":
        print("\n",pyfiglet.figlet_format("UnMapping  Edge  Nodes", width=180))
        nsx_failure_domain.get_failure_domain()
        nsx_edge_node.unmap_edge_node(nsx_failure_domain.dict_fd_id_name)

    # Print Edge cluster FD allocation policy
    elif choice == "7":
        print("\n",pyfiglet.figlet_format("Print  FD  Allocation", width=180))
        nsx_edge_cluster.get_edge_cluster()

    # Set edge cluster allocation policies
    elif choice == "8":
        print("\n",pyfiglet.figlet_format("Add  FD  Allocation", width=180))
        nsx_edge_node.get_edge_node()
        nsx_edge_cluster.update_edge_cluster()

    # Remove edge cluster allocation policies
    elif choice == "9":
        print("\n",pyfiglet.figlet_format("Remove  FD  Allocation", width=180))
        nsx_edge_cluster.remove_edge_fd_allocation()

    #Exit
    elif choice == "10":
        print("\n",pyfiglet.figlet_format("Logout", width=180))
        nsx_login.destroy_session()        
        sys.exit()

    else:
        print("\nWrong input. Enter valid Menu Item")

    run()

if __name__ == "__main__":
    run()