from google.cloud import resourcemanager_v3

def get_all_folders_in_org():
    ORGANIZATION_ID = '84503491758'  # Replace with your actual organization ID
    print(f"Listing folders for organization: {ORGANIZATION_ID}")

    client = resourcemanager_v3.FoldersClient()
    request = resourcemanager_v3.ListFoldersRequest(parent=f"organizations/{ORGANIZATION_ID}")
    
    try:
        page_result = client.list_folders(request=request)
        folders_list = []
        for folder in page_result:
            print(f"Found folder: {folder.name}")  # Corrected to folder
            folders_list.append(folder)
        return folders_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

get_folders = get_all_folders_in_org()

if get_folders:
    for folder in get_folders:
        print(folder.name)  # Assuming folder.name is the correct attribute for the folder ID
else:
    print("No folders found or there was an error listing folders.")  # Corrected to folders
