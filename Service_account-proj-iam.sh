#!/bin/bash

output_csv="gcp_service_accounts_permissions.csv"
# print header
echo "Project,ServiceAccount,Role,Member" > "$output_csv"

# Set timeout for gcloud commands
GCLOUD_TIMEOUT=300

# Get a list of all projects
PROJECTS=$(gcloud projects list --format="value(projectId)")

echo "Projects: $PROJECTS"

for project in $PROJECTS; do
    echo "Processing project: $project"
    # proj IAM
    project_iam=$(timeout $GCLOUD_TIMEOUT gcloud projects get-iam-policy "$project" --format=json)
    echo "Project IAM $project. Done!"

    # get svc acc
    service_accounts=$(timeout $GCLOUD_TIMEOUT gcloud iam service-accounts list --project="$project" --format="value(email)")
    echo "Service Accounts: $service_accounts"
    
    for service_account in $service_accounts; do
        echo "Processing service account: $service_account"

        # formating csv
        echo "$project_iam" | jq -r --arg sa "$service_account" --arg proj "$project" '
            .bindings[] | 
            select(.members[] | contains($sa)) | 
            .role as $role | 
            .members[] | 
            select(contains($sa)) | 
            [$proj, $sa, $role, .] | 
            @csv' >> "$output_csv"

    done
done

echo "Export completed: $output_csv"
