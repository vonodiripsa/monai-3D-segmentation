// This BICEP script will fully provision a functional federated learning sandbox
// based on simple internal silos secured with only Managed Identities.

// IMPORTANT: This setup is intended only for demo purpose. The data is still accessible
// by the users when opening the storage accounts, and data exfiltration is easy.

// For a given set of regions, it will provision:
// - an AzureML workspace and compute cluster for orchestration
// - per region, a silo (1 storage with 1 dedicated containers, 1 compute, 1 UAI)

// The demo permission model is represented by the following matrix:
// |               | orch.compute | siloA.compute | siloB.compute |
// |---------------|--------------|---------------|---------------|
// | orch.storage  |     R/W      |      R/W      |      R/W      |
// | siloA.storage |      -       |      R/W      |       -       |
// | siloB.storage |      -       |       -       |      R/W      |

// Usage (sh):
// > az login
// > az account set --name <subscription name>
// > az group create --name <resource group name> --location <region>
// > az deployment group create --template-file .\mlops\bicep\open_sandbox_setup.bicep \
//                              --resource-group <resource group name \
//                              --parameters demoBaseName="fldemo"

targetScope = 'resourceGroup'

// please specify the base name for all resources
@description('Base name of the demo, used for creating all resources as prefix')
param demoBaseName string = 'ams-mdemo'

// below parameters are optionals and have default values
// @allowed(['UserAssigned','SystemAssigned'])
// @description('Type of identity to use for permissions model')
// param identityType string = 'UserAssigned'

@description('Region of the orchestrator (workspace, central storage and compute).')
param orchestratorRegion string = resourceGroup().location

// @description('The VM used for creating compute clusters in orchestrator and silos.')
// param compute1SKU string = 'Standard_DS4_v2'

@description('Tags to curate the resources in Azure.')
param tags object = {
  Owner: 'AzureML Samples'
  Project: 'azure-ml-federated-learning'
  Environment: 'dev'
  Toolkit: 'bicep'
  Docs: 'https://github.com/Azure-Samples/azure-ml-federated-learning'
}

// Create Azure Machine Learning workspace
module workspace './modules/azureml/open_azureml_workspace.bicep' = {
  name: '${demoBaseName}-aml-${orchestratorRegion}'
  scope: resourceGroup()
  params: {
    defaultComputeName: 'monai-cluster'
    baseName: demoBaseName
    machineLearningName: 'aml-${demoBaseName}'
    machineLearningFriendlyName: 'Monai WS'
    machineLearningDescription: 'Azure ML demo workspace for federated learning (use for dev purpose only)'
    location: orchestratorRegion
    tags: tags
  }
}


