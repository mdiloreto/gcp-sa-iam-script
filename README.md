
# GCP Service Accounts Permissions Exporter

This script is designed to export the IAM permissions for service accounts across all projects within a Google Cloud Platform (GCP) organization and also for all your cloud assets using Google Cloud Assets API. It outputs the data in CSV format for easy auditing and review.

## Prerequisites
Before running this script, you will need the following:
- Enable Resource Manager, IAM and Cloud Assets APIs in GCP. 
- Access to a GCP account with the necessary permissions to view IAM policies and service accounts.
- The `gcloud` CLI installed and configured on your system.
- The `jq` utility for processing JSON.

## Setup

1. Clone the repository or download the script to your local machine.
2. Ensure that the `gcloud` CLI is authorized and configured with your GCP account. You can do this by running:
   ```sh
   gcloud auth login
   ```
3. Set the `organization_id` variable in the script to your GCP organization ID.

## Usage

Run the script in your terminal with the following command:

```sh
bash gcp_service_accounts_permissions_exporter.sh
```

The script will iterate through all projects within the specified organization ID, list service accounts, and fetch their IAM permissions.

## Output

The script generates two CSV files:

1. `gcp_service_accounts_permissions.csv` - Contains service account permissions for each project.
   ```csv
   Project,ServiceAccount,Role,Member
   ```
2. `service_accounts_iam_permissions_org.csv` - Contains service account permissions in al Assets at the organization level.
   ```csv
   Project,Folder,Resource,Member,Role
   ```

The CSV files will be saved in the current directory from which the script is executed.

## Contributing

If you have suggestions for improving the script, please open an issue or pull request.

## License

Specify your license here or state that the project is licensed under the MIT License (if applicable).
```
