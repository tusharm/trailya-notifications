from google.cloud import secretmanager

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()


def get_secret(secret_name: str):
    # Access the secret version.
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode('UTF-8')
