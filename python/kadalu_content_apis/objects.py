from kadalu_content_apis.helpers import response_object_or_error

class Document:
    def __init__(self, conn, bucket_name, path):
        """ Intialise Document/Object """
        self.conn = conn
        self.bucket_name = bucket_name
        self.path = path

    @classmethod
    def create(cls, conn, bucket_name, path, data, object_type, immutable, version, lock, template):
        """ Create object of both default("/") and with bucket-name """

        if bucket_name == "/":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/buckets/{bucket_name}/objects"
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
        return response_object_or_error("Object", resp, 201)


    @classmethod
    def list(cls, conn, bucket_name):
        """ List object(s) of both default("/") and with bucket-name """

        if bucket_name == "/":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/buckets/{bucket_name}/objects"

        resp = conn.http_get(url)
        return response_object_or_error("Bucket", resp, 200)


    # TODO: Handle empty responses
    # Ex: Pass non-existent object_name under root(/). Status Code = 200, But resp.data is empty
    def get(self):
        """ Return object of both default("/") and with bucket-name """

        if self.bucket_name == "/":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}"

        resp = self.conn.http_get(url)
        return response_object_or_error("Object", resp, 200)


    # TODO: Check for response once Object Update API is implemented
    def update(self, path=None, data=None, object_type=None, template=None):
        """ Update object of both default("/") and with bucket-name """

        if self.bucket_name == "/":
            url = f"{self.conn.url}/api/objects"
        else:
            url = f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}"

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

        return response_object_or_error("Object", resp, 200)


    def delete(self):
        """ Delete object of both default("/") and with bucket-name """

        if self.bucket_name == "/":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}"
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
