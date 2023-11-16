from google.cloud import resourcemanager_v3


def get_all_projects_in_folder():
    FOLDER_ID = '859893443547'  # Replace with your actual organization ID
    print(f"Listing projects for Folder: {FOLDER_ID}")

    client = resourcemanager_v3.ProjectsClient()
    request = resourcemanager_v3.ListProjectsRequest(
        parent=f"folders/{FOLDER_ID}"
    )
    
    try:
        page_result = client.list_projects(request=request)
        project_list = []
        for response in page_result:
            print(f"Found project: {response.project_id}")
            project_list.append(response.project_id)
        return project_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

get_projects = get_all_projects_in_folder()

if get_projects:
    for project_id in get_projects:
        print(project_id)
else:
    print("No projects found or there was an error listing projects.")

