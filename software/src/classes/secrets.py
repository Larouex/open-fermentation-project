# ==================================================================================
#   File:   secrets.py
#   Author: Larry W Jordan Jr (larouex@larouex.com)
#   Use:    Loads the secrets file
#
#   https://github.com/Larouex/open-fermentation-project
#
#   (c) 2022 Larouex Software Design LLC
#   This code is licensed under GNU license (see LICENSE.txt for details)
# ==================================================================================
import time, logging, string, json

# Azure IoT Libraries
from azure.keyvault.certificates import CertificateClient, CertificatePolicy,CertificateContentType, WellKnownIssuerNames
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.identity import ClientSecretCredential

class Secrets():

    def __init__(self, Log):

      # load file
      self.logger = Log
      self.data = []

      # creds
      self.credential = None
      self.secret_client = None

      # values to access
      self.provisioning_host = None
      self.scope_id = None
      self.device_primary_key = None
      self.device_secondary_key = None
      self.gateway_primary_key = None
      self.gateway_secondary_key = None

      # Initiate the Secrets
      self.load_file()

    # -------------------------------------------------------------------------------
    #   Function:   load_file
    #   Usage:      Load the Secrets.json file and execute __init()
    # -------------------------------------------------------------------------------
    def load_file(self):
      with open('secrets.json', 'r') as config_file:
        self.data = json.load(config_file)
        alerts = self.load_alerts()
        self.logger.debug(alerts["Alerts"]["Secrets"]["Loaded"].format(self.data))

      # Initiate the Secrets
      self.init()

      return

    # -------------------------------------------------------------------------------
    #   Function:   update_file_device_secrets
    #   Usage:      Append the passed Devices Data to the Secrets.json
    # -------------------------------------------------------------------------------
    def update_file_device_secrets(self, data):
        with open('secrets.json', 'w') as configs_file:
            alerts = self.load_alerts()
            self.logger.debug(alerts["Alerts"]["Secrets"]["Updated"].format(self.data))
            self.data["Devices"] = data
            configs_file.write(json.dumps(self.data, indent=2))

    # -------------------------------------------------------------------------------
    #   Function:   load_alerts
    #   Usage:      Simple logger info mapper
    # -------------------------------------------------------------------------------
    def load_alerts(self):
      with open('alerts.json', 'r') as alerts_file:
        return json.load(alerts_file)

    # -------------------------------------------------------------------------------
    #   Function:   private init
    #   Usage:      Sets up the property accessors and other meta-data
    # -------------------------------------------------------------------------------
    def init(self):

      self.provisioning_host = self.data["ProvisioningHost"]

      if self.data["UseKeyVault"]:

        self.logger.info("[USING KEY VAULT SECRETS]")

        # key vault account uri
        key_vault_uri = self.data["KeyVaultSecrets"]["KeyVaultUri"]
        self.logger.debug("[KEY VAULT URI] %s" % key_vault_uri)

        tenant_id = self.data["KeyVaultSecrets"]["TenantId"]
        client_id = self.data["KeyVaultSecrets"]["ClientId"]
        client_secret = self.data["KeyVaultSecrets"]["ClientSecret"]

        # Get access to Key Vault Secrets
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

        self.logger.debug("[credential] %s" % credential)
        self.logger.debug("[secret_client] %s" % secret_client)

        # Read all of our Secrets for Accessing IoT Central
        self.scope_id = self.secret_client.get_secret(self.data["KeyVaultSecrets"]["ScopeId"])
        self.device_primary_key = self.secret_client.get_secret(self.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"])
        self.device_secondary_key = self.secret_client.get_secret(self.data["KeyVaultSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"])
        self.gateway_primary_key = self.secret_client.get_secret(self.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"])
        self.gateway_secondary_key = self.secret_client.get_secret(self.data["KeyVaultSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"])

      else:

        # Read all of our LOCAL Secrets for Accessing IoT Central
        self.logger.info("[USING LOCAL SECRETS]")
        self.scope_id = self.data["LocalSecrets"]["ScopeId"]
        self.device_primary_key = self.data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"]
        self.device_secondary_key = self.data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Secondary"]
        self.gateway_primary_key = self.data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Primary"]
        self.gateway_secondary_key = self.data["LocalSecrets"]["GatewayConnect"]["SaSKeys"]["Secondary"]

      # Debug Only
      self.logger.debug("[SCOPE ID]: %s" % self.scope_id)
      self.logger.debug("[DEVICE PRIMARY KEY]: %s" % self.device_primary_key)
      self.logger.debug("[DEVICE SECONDARY KEY]: %s" % self.device_secondary_key)
      self.logger.debug("[GATEWAY PRIMARY KEY]: %s" % self.gateway_primary_key)
      self.logger.debug("[GATEWAY SECONDARY KEY]: %s" % self.gateway_secondary_key)

      return

    def get_provisioning_host(self):
      return self.provisioning_host

    def get_scope_id(self):
      return self.scope_id

    def get_device_primary_key(self):
      print(self.data["LocalSecrets"]["DeviceConnect"]["SaSKeys"]["Primary"])
      print(self.device_primary_key)
      return self.device_primary_key

    def get_device_secondary_key(self):
      return self.device_secondary_key

    def get_gateway_primary_key(self):
      return self.gateway_primary_key

    def get_gateway_secondary_key(self):
      return self.gateway_secondary_key

    def get_devices_secrets_data(self):
      return self.data["Devices"]

    def get_device_secrets(self, DeviceName):

      data = [x for x in self.data["Devices"] if x["Device"]["Name"] == DeviceName][0]
      return data


