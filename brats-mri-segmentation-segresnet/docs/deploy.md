# Run a MONAI Demo

In this tutorial, you will:

* Provision a fully functional environment in your own Azure subscription
* Run a sample federated learning pipeline in Azure ML

## Prerequisites

To enjoy this quick deployment, you will need to:

* have an active [Azure subscription](https://azure.microsoft.com) that you can use for development purposes,
* have permissions to create resources, set permissions, and create identities in this subscription (or at least in one resource group),
  * Note that to set permissions, you typically need _Owner_ role in the subscription or resource group - _Contributor_ role is not enough. This is key for being able to _secure_ the setup.
* [install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).

## Deploy demo resources in Azure

### One click ARM deployment

Click on the buttons below depending on your goal. It will open in Azure Portal a page to deploy the resources in your subscription.

| Button | Description |
| :-- | :-- |
| [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fvonodiripsa%2Fmonai-3D-segmentation%2Fmain%2Fbrats-mri-segmentation-segresnet%2Fdeployment%2Farm%2Fmonai-setup.json) | This setup is intended only for demo purposes. The data is still accessible by the users of your subscription when opening the storage accounts, and data exfiltration is possible. |

> Notes:
>
> * If someone already provisioned a demo with the same name in your subscription, change **Demo Base Name** parameter to a unique value.
> * If you need to provision GPU's instead of CPU's, you can just use a GPU SKU value for the "Compute SKU" parameter, `Standard_NC12s_v3` for instance. An overview of the GPU SKU's available in Azure can be found [here](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes-gpu). Beware though, SKU availability may vary depending on the region you choose, so you may have to use different Azure regions instead of the default ones.


## Launch the demo experiment

In this section, we'll use a sample python script to submit a MONAI learning experiment to Azure ML. The script will need to connect to your newly created Azure ML workspace first.

1. Create a conda environment with all the python dependencies, then activate it.

    ```bash
    conda env create --file ./examples/pipelines/environment.yml
    conda activate fl_experiment_conda_env
    ```

    Alternatively, you can install the dependencies directly:

    ```bash
    python -m pip install -r ./examples/pipelines/requirements.txt
    ```

2. To connect to your newly created Azure ML workspace, you'll need to provide the following info in the sample python script as CLI arguments.

    ```bash
    python ./examples/pipelines/fl_cross_silo_literal/submit.py --subscription_id <subscription_id> --resource_group <resource_group> --workspace_name <workspace_name> --example MNIST
    ```
    > Notes: 
        > * You can use --offline flag when running the job to just build and validate pipeline without submitting it.
        > * Differential privacy is disabled by default, but you can quickly turn it on by setting the `config.yaml` file's `dp` parameter to `true`.
    
    Note: you can also create a `config.json` file at the root of this repo to provide the above information. Follow the instructions on how to get this from the [Azure ML documentation](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-configure-environment#workspace).

    ```json
    {
        "subscription_id": "<subscription-id>",
        "resource_group": "<resource-group>",
        "workspace_name": "<workspace-name>"
    }
    ```
