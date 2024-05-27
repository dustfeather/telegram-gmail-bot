# Python Gmail Summary Bot

## Creating a service account for accessing Google APIs.

### Step 1: Create a Service Account

1. **Go to the Google Cloud Console**: [Google Cloud Console](https://console.cloud.google.com/).
2. **Select your project** or create a new one.
3. **Navigate to the Service Accounts page**:
    - Go to the "IAM & Admin" section.
    - Click on "Service Accounts".
4. **Create a Service Account**:
    - Click on "Create Service Account".
    - Enter a name and description for the service account.
    - Click "Create and Continue".
5. **Grant the service account access to the project**:
    - Select a role for the service account (e.g., "Editor" or any other role appropriate for your needs).
    - Click "Continue".
6. **Create key**:
    - Click on "Done" and then find your newly created service account in the list.
    - Click on the service account, then go to the "Keys" tab.
    - Click "Add Key" and select "Create new key".
    - Choose "JSON" and click "Create".
    - A JSON file containing your private key will be downloaded. Keep this file secure.

### Step 2: Enable the Gmail API

1. **Go to the API & Services page**: [API & Services](https://console.cloud.google.com/apis/dashboard).
2. **Enable the Gmail API**:
    - Click on "Enable APIs and Services".
    - Search for "Gmail API" and enable it for your project.

> [!WARNING]
> I recommend just forking the repo and using it as a GitHub Action

## Local usage

```shell
cp .env.example .env
```

```shell
python3 -m venv .
python3 -m pip install -r requirements.txt
python3 main.py
```