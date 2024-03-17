from json import dumps
from boto3 import Session
from helper import get_ms, get_dt

class Loader:

    def __init__(self) -> None:
        pass

    def load(self, session: Session, processed_responses: list[str]):
        s3 = session.resource("s3")
        for response in processed_responses:
            s3.Object(get_dt(), f"{response.get('ticker')}{get_ms()}.json").put(
                Body=dumps(response)
            )
