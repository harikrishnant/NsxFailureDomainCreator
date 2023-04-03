# NsxFailureDomainCreator
NSX Failure Domain Creator will automate the below tasks when working with NSX Edge Failure Domains:
- Listing available failure domains
- Creating failure domains
- Deleting failure domains
- Print edge nodes and dge cluster information
- Mapping edge nodes to failure domains
- Unmapping edge nodes from failure domains
- Setting allocation plocy to edge clusters

**Tested NSX versions**
1. NSX-T 2.X
2. NSX-T 3.X
3. NSX 4.X

# Instructions
1. Install Python3. On CentOS or RHEL systems, run -> *yum install -y python3*
2.  Install git -> *yum install -y git*
3.  Install the below python modules:
     - requests -> *python3 -m pip install requests*
     - urllib3 -> *python3 -m pip install urllib3* 
     - tabulate -> *python3 -m pip install tabulate*
     - pyfiglet -> *python3 -m pip install pyfiglet*
4. Clone the repository and navigate to NsxAlbCloudMigrator/V1.1/ -> 
   *git clone https://github.com/harikrishnant/NsxFailureDomainCreator.git && cd NsxFailureDomainCreator*
5. Run *python3 failure_domain_creator.py -i <NSX Manager IP/FQDN> -u <NSX_user> -p <NSX_user_password>* and follow the instructions in the menu screeen

![61](https://user-images.githubusercontent.com/35589049/229488601-92c7a65f-d18d-430f-bede-3d1f4dbf27c3.png)

# Contact
Please contact me at https://vxplanet.com for improvising the code, feature enhancements and bugs. Alternatively you can also use Issue Tracker to report any bugs or questions regarding the NSXFailureDomainCreator tool. 

![VxPlanet.com](https://serveritpro.files.wordpress.com/2021/09/vxplanet_correct.png)
