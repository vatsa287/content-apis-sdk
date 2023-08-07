# noqa # pylint: disable=missing-module-docstring
from kadalu_content_apis.regions import Region
from kadalu_content_apis.folders import Folder
from kadalu_content_apis.objects import Document
from kadalu_content_apis.templates import Template
from kadalu_content_apis.helpers import ConnectionBase, APIError, json_from_response

class Connection(ConnectionBase):
    def __init__(self, url, username=None, email=None, password=None, user_id=None, token=None):
        """Intialise Connection and Login to Kadalu Content API"""
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

        if email is not None and password is not None:
            resp = self.http_post(self.url + "/api/api-keys", {"email": email, "password": password})

            # TODO: Send correct error response from API when email/password/etc are wrong
            # Currently response data seems to be empty.
            # if resp.status != 201:
            #     raise APIError(resp)

            resp_json = json_from_response(resp)

            self.user_id = resp_json["user_id"]
            self.token = resp_json["token"]

        if user_id is not None and token is not None:
            self.user_id = user_id
            self.token = token


    def create_region(self, name, address):
        """ Create a new region """
        return Region.create(self, name, address)


    def create_folder(self, name, region="", immutable=False, version=False, lock=False, template=None):
        """ Create a new folder """
        return Folder.create(self, name, region, immutable, version, lock, template)


    def list_folders(self):
        """ Return list of folders """
        return Folder.list_folders(self)


    def folder(self, name):
        return Folder(self, name)


    def create_object(self, path, data, object_type, immutable=False, version=False, lock=False):
        """ Create default("/") object """
        return Document.create(self, "/", path, data, object_type, immutable, version, lock)


    def list_objects(self):
        """ List all default("/") objects """
        return Document.list(self, "/")

    def object(self, path):
        """ Return Object/Document instance """
        return Document(self, "/", path)

    def create_template(self, name, content, template_type, output_type="text", public=False):
        """ Create Template """
        return Template.create(self, name, content, template_type, output_type, public)

    def list_templates(self):
        """ List all templated """
        return Template.list_templates(self)

    def template(self, name):
        """ Return Template instance """
        return Template(self, name)
