import argparse
import logging
import sys
import os
import shutil
import tarfile


#downloaded_path = './tmp'

def run1(args) -> str:
    """Run script with arguments (the core of the component).

    Args:
        inputs:
        blob_file_location:
            type: uri_folder
            description: the input blob .tar file location
            mode="ro_mount"
        overwrite:
            type: boolean
            description: overwrire local data
            default: true
            optional: true       

        outputs:    
        image_data_folder:
            type: uri_folder
            description: the output folder where the uncompressed data will be written
            mode="rw_mount"    
    """

    #cur_dir = os.getcwd()

    r_dir = './'

    image_data_folder='/tmp/bt_uncompressed_images'
    if not os.path.exists(image_data_folder):
        os.mkdir(image_data_folder)
    os.chdir(image_data_folder)

    print(f"Compressed data path: {args.blob_file_location}")  

    logging.info(f"Uncompressed images path: {image_data_folder}")  
    logging.info(f"Compressed data path: {args.blob_file_location}")  

    with tarfile.open(args.blob_file_location, "r") as tar:
        tar.extractall(path=r_dir)

    args.image_data_folder = os.getcwd()

    i_f = [f for f in os.listdir(args.image_data_folder) if os.path.isdir(os.path.join(args.image_data_folder, f))]
    print(f"Uncompressed images path: {args.image_data_folder}")  
    print(f'{len(i_f)} images in image_folders.')

    
    # for path in os.listdir(image_data_folder):
    #     # check if current path is a file
    #     if os.path.isfile(os.path.join(dir_path, path)):
    #         res.append(path)
        
    # print(res)  


def run(args) -> str:    

    # create directory if it doesn't exist yet

    # compressed_file = os.path.join(args.image_data_folder, 'braintumor/BraTS2021_Training_Data.tar')

    # uncompressed_folder = os.path.join(args.image_data_folder, 'uncompressed')

    # os.makedirs(args.image_data_folder, exist_ok=True)

    # # print for debugging
    # logging.info(f"Uncompressed images path: {ancompressed_folder}") 
    # logging.info(f"Compressed data path: {compressed_file}")

    # extract 
    with tarfile.open(args.blob_file_location, "r") as tar:
        tar.extractall(path=args.image_data_folder)
   
    # i_f = [f for f in os.listdir(uncompressed_folder) if os.path.isdir(os.path.join(uncompressed_folder, f))]

    # print(f'{len(i_f)} images in image_folders.')

    # arg.image_data_folder = uncompressed_folder


def get_arg_parser(parser=None):
    """Parse the command line arguments for merge using argparse.
    Args:
                inputs:
                blob_file_location:
                    type: uri_folder
                    description: the input blob .tar file location
                    mode="ro_mount"
                overwrite:
                    type: boolean
                    description: overwrire local data
                    default: true
                    optional: true       

                outputs:    
                image_data_folder:
                    type: uri_folder
                    description: the output folder where the uncompressed data will be written
                    mode="rw_mount"    
    """
    # add arguments that are specific to the component
    if parser is None:
        parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--blob_file_location",
        type=str,
        required=True,
        help="Azure blob name",
    )

    parser.add_argument(
        "--overwrite",
        type=bool,
        required=False,
        help="Overwrite files",
    )
    parser.add_argument(
        "--image_data_folder",
        type=str,
        required=True,
        help="Location of results",
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

    logging.info(f"Running script with arguments: {args}")
    # args.image_data_folder = run(args)
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