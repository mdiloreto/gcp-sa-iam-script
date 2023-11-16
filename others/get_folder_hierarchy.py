from google.cloud import resourcemanager_v3

def get_folders_hierarchy(client, parent, path=""):
    """
    Recursively get the hierarchy of folders.
    """
    request = resourcemanager_v3.ListFoldersRequest(parent=parent)
    response = client.list_folders(request=request)

    hierarchy = []

    for folder in response:
        # Construct the full path for the current folder
        current_path = f"{path}/{folder.display_name}" if path else folder.display_name
        print(f"Folder Path: {current_path}, Folder ID: {folder.name}")
        
        # Recursively get subfolder hierarchy
        sub_hierarchy = get_folders_hierarchy(client, folder.name, current_path)
        hierarchy.append({
            'name': folder.display_name,
            'id': folder.name,
            'path': current_path,
            'subfolders': sub_hierarchy
        })

    return hierarchy

# Recursive function to print the folder hierarchy
def print_hierarchy(hierarchy, level=0):
    indent = "  " * level  # Two spaces per level of depth
    for folder in hierarchy:
        print(f"{indent}- {folder['name']} (ID: {folder['id']}, Path: {folder['path']})")
        if folder['subfolders']:  # If there are subfolders, go deeper
            print_hierarchy(folder['subfolders'], level + 1)

# Initialize client
client = resourcemanager_v3.FoldersClient()

# Replace with your organization ID
ORGANIZATION_ID = '84503491758'

# Start the recursive function from the organization level
full_hierarchy = get_folders_hierarchy(client, f"organizations/{ORGANIZATION_ID}")

# The full_hierarchy variable now contains the hierarchical structure of folders
print_hierarchy(full_hierarchy)
