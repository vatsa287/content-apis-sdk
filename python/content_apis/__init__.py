# noqa # pylint: disable=missing-module-docstring
from content_apis.regions import Region
from content_apis.buckets import Bucket
from content_apis.helpers import ConnectionBase, APIError, json_from_response

class Connection(ConnectionBase):
    """Content API Instance"""

    def __init__(self, url, username=None, password=None, user_id=None, token=None):
        self.url = url.strip("/")
        super().__init__()

        if username is not None and password is not None:
            resp = self.http_post(self.url + "/api/api-keys", {"username": username, "password": password})

            # TODO: Send correct error response from API when username/password/etc are wrong
            # Currently response data seems to be empty.
            # if resp.status != 201:
            #     raise APIError(resp)

            resp_json = json_from_response(resp)

            self.user_id = resp_json["user_id"]
            self.token = resp_json["token"]

            print(self.user_id, self.token)

        if user_id is not None and token is not None:
            self.user_id = user_id
            self.token = token

    def create_region(self, name, address):
        return Region.create(self, name, address)

    def create_bucket(self, name, region, immutable=False, version=False, lock=False):
        return Bucket.create(self, name, region, immutable, version, lock)

    # def list_buckets(self):
    #     return Bucket.list(self)

    # def bucket(self, name):
    #     return Bucket(self, name)
