from google.cloud import resourcemanager_v3
from googleapiclient import discovery
from google.oauth2 import service_account  # type: ignore
from oauth2client.client import GoogleCredentials
import os
from google.cloud import asset_v1


################################
#>>>>>> Define functions <<<<<<#
################################

# >>>>>>>>>>>>>>>> GET Folders Hierarchy <<<<<<<<<<<<<<<<<<<

from google.cloud import resourcemanager_v3

def get_folders_hierarchy(client, parent, path="", folders_id_list=None):
    if folders_id_list is None:
        folders_id_list = []

    request = resourcemanager_v3.ListFoldersRequest(parent=parent)
    response = client.list_folders(request=request)

    hierarchy = []

    for folder in response:
        # Construct the full path for the current folder
        current_path = f"{path}/{folder.display_name}" if path else folder.display_name
        print(f"Folder Path: {current_path}, Folder ID: {folder.name}")

        # Add the folder ID (not display name) to the list
        folder_id = folder.name.split('/')[1]  # Extract the ID part
        folders_id_list.append(folder_id)

        # Recursively get subfolder hierarchy
        sub_hierarchy = get_folders_hierarchy(client, folder.name, current_path, folders_id_list)
        hierarchy.append({
            'name': folder.display_name,
            'id': folder.name,
            'path': current_path,
            'subfolders': sub_hierarchy
        })

    return folders_id_list

# >>>>>>>>>>>>>>>> Print Folders Hierarchy <<<<<<<<<<<<<<<<<<<

def print_hierarchy(hierarchy, level=0):
    indent = "  " * level  # Two spaces per level of depth
    for folder in hierarchy:
        print(f"{indent}- {folder['name']} (ID: {folder['id']}, Path: {folder['path']})")
        if folder['subfolders']:  # If there are subfolders, go deeper
            print_hierarchy(folder['subfolders'], level + 1)
            
# >>>>>>>>>>>>>>>>> [NOT IN USE] get folders ID List <<<<<<<<<<<<<<<<<<
    ####### this gets done in get_folders_hierarchy function #######
def get_folder_ids_from_hierarchy(hierarchy, folder_ids_list):
    for folder in hierarchy:
        # Assuming 'id' is the key that contains the folder's ID in the format "folders/{folder_id}"
        folder_id = folder['id'].split('/')[1]  # This will extract just the numerical ID
        folder_ids_list.append(folder_id)
        # If the folder has subfolders, we recursively get their IDs too
        if folder['subfolders']:
            get_folder_ids_from_hierarchy(folder['subfolders'], folder_ids_list)
    
    return folder_ids_list

# >>>>>>>>>>>>>>>> GET Projects in each folder <<<<<<<<<<<<<<<<<<<

def get_all_projects_in_folder(client, folder_ids_list):
    project_list = []
    
    for folder in folder_ids_list:        
        print(f"Listing projects for Folder: {folder}")
        request = resourcemanager_v3.ListProjectsRequest(
            parent=f"folders/{folder}"
        )
        page_result = client.list_projects(request=request)      
        for response in page_result:
            print(f"Found project: {response.project_id}")
            project_list.append(response.project_id)
    
    return project_list

# def list_service_accounts(proj_list):
#     """Lists all service accounts for the current project."""
#     credentials = GoogleCredentials.get_application_default()
#     service = discovery.build('iam', 'v1', credentials=credentials)
#     service_accounts = []
#     for proj in proj_list:
#         request = service.projects().serviceAccounts().list(name='projects/' + proj)
#         while True:
#             response = request.execute()

#             for service_account in response.get('accounts', []):
#                 # Process each `service_account` resource:
#                 service_accounts.append(service_account)

#             request = service.projects().serviceAccounts().list_next(previous_request=request, previous_response=response)
#             if request is None:
#                 print(f"No more service accounts in project {proj}")
#                 break
#     return service_accounts

def list_service_accounts2(proj_list):
    """Lists all service accounts for the current project."""

    service_accounts_list = []
    service = discovery.build('iam', 'v1')
    
    for proj in proj_list:
        request = service.projects().serviceAccounts().list(name='projects/' + proj)
        # Handle pagination
        while request is not None:
            response = request.execute()
            service_accounts = response.get('accounts', [])
            
            for account in service_accounts:
                service_accounts_list.append(account['name'])
            
            request = service.projects().serviceAccounts().list_next(
                previous_request=request, previous_response=response)
            
    return service_accounts_list

def get_all_proj_assets(client, proj_list):
       
    assets_list = []
    for proj in proj_list:
        # Initialize request argument(s)
        request = asset_v1.SearchAllResourcesRequest(
            scope=f"projects/{proj}",
        )

        # Make the request
        page_result = client.search_all_resources(request=request)

        # Handle the response
        for response in page_result:
            print(f"Found Asset: {response.name}")
            assets_list.append(response.name)
    
    return assets_list

def get_all_proj_assets2(client):
    assets_list2 = []
    
    # Exclude specific services like service usage, logging, etc.
    exclude_services_filter = (
        'NOT name:"//serviceusage.googleapis.com/" AND '
        'NOT name:"//logging.googleapis.com/"'
        'NOT name:"iam.googleapis.com/"'
    )
    # Initialize request argument(s)
    request = asset_v1.SearchAllResourcesRequest(
        scope=f"organizations/{ORGANIZATION_ID}",
        query=exclude_services_filter
    )

    # Make the request
    page_result = client.search_all_resources(request=request)

    # Handle the response
    for response in page_result:
        print(f"Found Asset: {response.name}")
        assets_list2.append(response.name)
    
    return assets_list2

################################
#>>>>>>>>>> EXECUTE <<<<<<<<<<<#
################################

# 0. Initialize client
client_folders = resourcemanager_v3.FoldersClient()
client_projects = resourcemanager_v3.ProjectsClient()

# 1. Input organizationid
ORGANIZATION_ID = '84503491758'

# 2. Start recursive folder hierarchy
folders_id_list = get_folders_hierarchy(client_folders, f"organizations/{ORGANIZATION_ID}")

# 3.a Get projects from each folder id (from folders_id_list)
get_projects = get_all_projects_in_folder(client_projects, folders_id_list)

# 3.b print projects
if get_projects:
    for project_id in get_projects:
        print(project_id)
else:
    print("No projects found or there was an error listing.")

# 4.a Get service Accounts
get_service_accounts = list_service_accounts2(get_projects)

# 4.b print service accounts
if get_service_accounts:
    for service_account in get_service_accounts:
        print(service_account)
else:
    print("No Service Accounts found or there was an error listing.")

# 5. Get all assets in all the projects using the Google Cloud Assets API
    # 5.a. Get Client 
client_assets = asset_v1.AssetServiceClient()
    # 5.b. Execute funciton
get_assests2 = get_all_proj_assets2(client_assets)

    #### 5.test. TEST #######
# get_projects_test = []
# get_projects_test.append("715047386127")
# get_assests = get_all_proj_assets(client_assets, get_projects_test)
    #### END TEST ###########
    
if get_assests2:
    for asset in get_assests2:
        print(asset)
else:
    print("No Assets were found or there was an error listing.")
    
# if get_assests:
#     for asset in get_assests:
#         print(asset.name)
# else:
#     print("No Assets were found or there was an error listing.")