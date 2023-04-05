# Run the MONAI Demo

In this tutorial, you will:

* Provision a fully functional environment in your own Azure subscription
* Run a sample of MONAI machine learning pipeline in Azure ML

it is based on the following MONAI tutorial: https://github.com/Project-MONAI/tutorials/blob/main/3d_segmentation/brats_segmentation_3d.ipynb

## Prerequisites

To enjoy this quick deployment, you will need to:

* have an active [Azure subscription](https://azure.microsoft.com) that you can use for development purposes,
* have permissions to create resources, set permissions, and create identities in this subscription (or at least in one resource group),
  * Note that to set permissions, you typically need _Owner_ role in the subscription or resource group - _Contributor_ role is not enough. This is key for being able to _secure_ the setup.
* [install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

## Deploy demo resources in Azure

### One click ARM deployment

Click on the button below. It will open in Azure Portal a page to deploy the resources in your subscription.

| Button | Description |
| :-- | :-- |
| [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fvonodiripsa%2Fmonai-3D-segmentation%2Fmain%2Fbrats-mri-segmentation-segresnet%2Fdeployment%2Farm%2Fmonai-setup.json) | This setup is intended only for demo purposes. The data is still accessible by the users of your subscription when opening the storage accounts, and data exfiltration is possible. |

> Notes:
>
> * If someone already provisioned a demo with the same name in your subscription, change **Demo Base Name** parameter to a unique value.
> * For provisioning GPU or CPU, you need just use a GPU/CPU SKU value for the "Compute SKU" parameter, `Standard_NC12s_v3` for instance. An overview of the GPU SKU's available in Azure can be found [here](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes-gpu). Beware though, SKU availability may vary depending on the region you choose, so you may have to use different Azure regions instead of the default ones.


## Launch the demo experiment

We'll use notebooks to orchestrate the demo. Once you will create the environment you need to create provided notebooks, components and prepare the demo data set (.tar)
