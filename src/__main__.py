import os, helper
from argparse import ArgumentParser
from src.extractor import Extractor
from src.processor import Processor
from src.loader import Loader

ENV                   = os.getenv("ENV", "dev")
CONFIG_PATH           = os.getenv("CFG", "src/config.yaml")
CONFIG                = helper.parse_config(CONFIG_PATH).get(ENV)
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_LOCATION  = os.getenv("AWS_DEFAULT_LOCATION", "us-west-1")

if (__name__ == "__main__" and all([CONFIG,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_DEFAULT_LOCATION])):
    args_parser = ArgumentParser()
    extractor   = Extractor()
    processor   = Processor()
    loader      = Loader()

    args_parser.add_argument('-ts', '--tickers')
    args          = args_parser.parse_args()
    tickers       = args.tickers.split(",")
    raw_responses = extractor.extract(tickers=tickers)

    if raw_responses:
        processed_responses = processor.process(raw_responses)
        aws_session = helper.create_AWS_session(aws_access_key_id=AWS_ACCESS_KEY_ID, 
                                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3_bucket = helper.create_S3_bucket(session=aws_session, 
                                            bucket_name=helper.get_dt(), 
                                            bucket_location=AWS_DEFAULT_LOCATION)
        loader.load(session=aws_session, processed_responses=processed_responses)
