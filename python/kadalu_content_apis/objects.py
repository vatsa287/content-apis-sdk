import os
from kadalu_content_apis.shares import Share
from kadalu_content_apis.helpers import response_object_or_error, APIError, Generic

class Document(Generic):
    def __init__(self, conn=None, folder_name=None, path=None, data={}):
        """ Intialise Document/Object """
        super().__init__(data)

        if conn is not None:
            self.conn = conn

        if folder_name is not None:
            self.folder_name = folder_name

        if path is not None:
            self.path = path


    @classmethod
<<<<<<< HEAD
    def create(cls, conn, folder_name, path, data, object_type, immutable, version, lock, template):
        """ Create object of both default("/") and with folder-name """
=======
    def create(cls, conn, bucket_name, path, data, object_type, immutable, version, lock, template):
        """ Create object of both default("/") and with bucket-name """
>>>>>>> python: Add get_rendered()

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"
        resp = conn.http_post(
            url,
            {
                "path": path,
                "type": object_type,
                "data": data,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
            }
        )
        outdata = response_object_or_error(Document, resp, 201)
        outdata.conn = conn
        outdata.folder_name = folder_name
        return outdata

    @classmethod
    def upload(cls, conn, folder_name, file_path, object_type, path, immutable, version, lock, template):
        """ Upload object data at file_path """

        file_content = ""

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"

        with open(file_path, "r") as file:
            file_content = file.read()

        # If path is empty, set filepath as path excluding the relative path
        if path == "":
            path = os.path.basename(file_path)

        meta = {
                "path": path,
                "type": object_type,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
        }

        resp = conn.http_post_upload(
            url,
            meta, file_path, file_content
        )
        outdata = response_object_or_error(Document, resp, 201)
        outdata.conn = conn
        outdata.folder_name = folder_name
        return outdata


    @classmethod
    def list(cls, conn, folder_name):
        """ List object(s) of both default("/") and with folder-name """

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"

        resp = conn.http_get(url)
        objects = response_object_or_error(Document, resp, 200)

        def update_conn(obj):
            obj.conn = conn
            obj.folder_name = folder_name
            return obj

        return list(map(update_conn, objects))


    # TODO: Handle empty responses
    # Ex: Pass non-existent object_name under root(/). Status Code = 200, But resp.data is empty
    def get(self):
        """ Return object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"

        resp = self.conn.http_get(url)

        outdata = response_object_or_error(Document, resp, 200)
        outdata.conn = self.conn
        outdata.folder_name = self.folder_name
        return outdata


    # TODO: Check for response once Object Update API is implemented
    def update(self, path=None, data=None, object_type=None, template=None):
<<<<<<< HEAD
        """ Update object of both default("/") and with folder-name """
=======
        """ Update object of both default("/") and with bucket-name """
>>>>>>> python: Add get_rendered()

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/objects"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"

        resp = self.conn.http_put(
            url,
            {
                "path": path,
                "data": data,
                "type": object_type,
                "template": template
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and path is not None:
            self.path = path

        outdata = response_object_or_error(Document, resp, 200)
        outdata.conn = self.conn
        outdata.folder_name = self.folder_name
        return outdata

    def delete(self):
        """ Delete object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if self.folder_name == "":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"
        resp = self.conn.http_delete(url)
        return response_object_or_error("Object", resp, 204)


    def get_rendered(self, template=None):
        """ Return rendered of both default("/") and with bucket-name """

        if self.bucket_name == "/":
            url = f"{self.conn.url}/api/content/objects/{self.path}?{template}"
        else:
            url = f"{self.conn.url}/api/content/buckets/{self.bucket_name}/objects/{self.path}?{template}"

        resp = self.conn.http_get(url)

        # TODO: Send response in correct way
        # return response_object_or_error("Object", resp, 200)
        if resp.status != 200:
            raise APIError(resp)
        return resp.data
