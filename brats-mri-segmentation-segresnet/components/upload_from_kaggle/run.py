import argparse
import logging
import sys
import os
import shutil

from azureml.core import Run, Workspace
from azureml.core.keyvault import Keyvault


def get_kaggle_client(kv: Keyvault):
    """Gets a Kaggle client using the secrets in a key vault to authenticate.
    Args:
        kv (Keyvault): key vault to use for retrieving the Kaggle credentials. The Kaggle user name secret needs to be named 'kaggleusername', while the Kaggle API key secret needs to be named 'kagglekey'.
    """

    os.environ["KAGGLE_USERNAME"] = kv.get_secret("kaggleusername")
    os.environ["KAGGLE_KEY"] = kv.get_secret("kagglekey")

    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    return api


def get_key_vault() -> Keyvault:
    """Retrieves key vault from current run"""
    run: Run = Run.get_context()
    logging.info(f"Got run context: {run}")
    workspace: Workspace = run.experiment.workspace
    return workspace.get_default_keyvault()


def download_unzip_kaggle_dataset(
    kaggle_client, path, dataset_name="paultimothymooney/chest-xray-pneumonia"
):
    """Download a dataset to a specified location and unzip it
    Args:
        kaggle_client (KaggleApi): Instance of KaggleApi to use for retrieving the dataset
        path(str): location where to store downloaded dataset
        dataset_name (str): the name of the dataset to download ('paultimothymooney/chest-xray-pneumonia' by default)
    """
    kaggle_client.dataset_download_files(dataset=dataset_name, path=path, unzip=True)


def run(args):
    """Run script with arguments (the core of the component).

    Args:
        args (argparse.namespace): command line arguments provided to script
    """

    # # get the key vault associated to the current workspace
    # kv = get_key_vault()

    # # authenticate to Kaggle using the secrets in the key vault
    # kaggle_client = get_kaggle_client(kv)
    kaggle_client = get_kaggle_client()

    # download and unzip the dataset
    download_unzip_kaggle_dataset(kaggle_client, args.image_data_folder, args.kaggle_dataset)

   
def get_arg_parser(parser=None):
    """Parse the command line arguments for merge using argparse.
    Args:
        parser (argparse.ArgumentParser or CompliantArgumentParser):
        an argument parser instance
    Returns:
        ArgumentParser: the argument parser instance
    Notes:
        if parser is None, creates a new parser instance
    """
    # add arguments that are specific to the component
    if parser is None:
        parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--kaggle_datset",
        type=str,
        required=True,
        help="Dataset name",
    )
    parser.add_argument(
        "--data_folder",
        type=str,
        required=True,
        help="Output folder for data",
    )
    return parser


def main(cli_args=None):
    """Component main function.
    It parses arguments and executes run() with the right arguments.
    Args:
        cli_args (List[str], optional): list of args to feed script, useful for debugging. Defaults to None.
    """

    # build an arg parser
    parser = get_arg_parser()

    # run the parser on cli args
    args = parser.parse_args(cli_args)

    print(f"Running script with arguments: {args}")
    run(args)


if __name__ == "__main__":
    # Set logging to sys.out
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(log_format)
    logger.addHandler(handler)

    main()