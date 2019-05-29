import os
from azure.mgmt.compute import ComputeManagementClient
import azure.mgmt.resource
import automationassets
import sys
import json

webhookpayload = sys.argv[1]
value = json.loads(webhookpayload)
requestBody = json.loads(value["RequestBody"])
schemaType = requestBody["schemaId"]

if schemaType == "AzureMonitorMetricAlert":
    print "AzureMonitorMetricAlert"
    print requestBody["data"]["context"]["resourceName"]
elif schemaType == "Microsoft.Insights/activityLogs":
    print "Microsoft.Insights/activityLogs"
    print requestBody["data"]["context"]["activityLog"]["resourceId"]
elif schemaType == "":
    print "Original"
    print requestBody["context"]

def get_automation_runas_credential(runas_connection):
    from OpenSSL import crypto
    import binascii
    from msrestazure import azure_active_directory
    import adal

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    pks12_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM,pks12_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    resource ="https://management.core.windows.net/"
    authority_url = ("https://login.microsoftonline.com/"+tenant_id)
    context = adal.AuthenticationContext(authority_url)
    return azure_active_directory.AdalAuthentication(
    lambda: context.acquire_token_with_client_certificate(
            resource,
            application_id,
            pem_pkey,
            thumbprint)
    )

    
# Authenticate to Azure using the Azure Automation RunAs service principal
runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
azure_credential = get_automation_runas_credential(runas_connection)

# print(sys.argv[0])
# print(sys.argv[1])