// This BICEP script will fully provision MONAI sandbox

// Usage (sh):
// > az login
// > az account set --name <subscription name>
// > az group create --name <resource group name> --location <region>
// > az deployment group create --template-file .\deployment\bicep\open_sandbox_setup.bicep \
//                              --resource-group <resource group name \
//                              --parameters demoBaseName="MONAI-3D"

targetScope = 'resourceGroup'

// please specify the base name for all resources
@description('Base name of the demo, used for creating all resources as prefix')
param demoBaseName string = 'MONAI-3D'

// below parameters are optionals and have default values
// @allowed(['UserAssigned','SystemAssigned'])
// @description('Type of identity to use for permissions model')
// param identityType string = 'UserAssigned'

// @description('Region of the orchestrator (workspace, central storage and compute).')
param workspaceRegion string = resourceGroup().location

// Create Azure Machine Learning workspace
module workspace './modules/azureml/open_azureml_workspace.bicep' = {
  name: '${demoBaseName}-aml-${workspaceRegion}'
  scope: resourceGroup()
  params: {
    defaultComputeName: 'monai-cluster'
    baseName: demoBaseName
    machineLearningName: 'aml-${demoBaseName}'
    machineLearningFriendlyName: 'MONAI WS'
    machineLearningDescription: 'Azure ML MONAI demo workspace (use for dev purpose only)'
    location: workspaceRegion
  }
}


