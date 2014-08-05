import hmac
import base64
import hashlib
import datetime
import requests

VERSION = '0.0.2'
USER_AGENT = 'summoner v%s <http://github.com/edsu/summoner>' % VERSION

class Summon():

    def __init__(self, access_id, secret_key):
        self.access_id = access_id
        self.secret_key = secret_key
        self.host = 'api.summon.serialssolutions.com'


    def status(self):
        r = self._get("/2.0.0/search/ping")
        if 'status' in r:
            return r['status']


    def search(self, q, **kwargs):
        """
        You can pass in any of the Summon Search API parameters 
        (without the "s." prefix). For example to remove highlighting:

            result = api.search("Web", hl=False)

        See the Summon API documentation for the full list of possible
        parameters:

        http://api.summon.serialssolutions.com/help/api/search/parameters
        """
        params = {"s.q": q}
        for k, v in kwargs.items():
            params["s." + k] = v
        r = self._get("/2.0.0/search", params)
        return r


    def _get(self, path, params={}):
        now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'application/json',
            'Host': self.host,
            'x-summon-date': now,
            'x-summon-session-id': ''
        }

        # generate auth token
        id_str = self._id_string(path, params, headers)
        hash_code = hmac.new(self.secret_key, id_str, hashlib.sha1)
        hash_code_digest = base64.encodestring(hash_code.digest())
        auth = "Summon %s;%s" % (self.access_id, hash_code_digest)
        headers['Authorization'] = auth

        url = "http://%s%s" % (self.host, path)
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


    def _id_string(self, path, params, headers):
        if len(params) > 0:
            q_parts = []
            for k, vals in params.items():
                # TODO: urlencode params?
                if type(vals) != list:
                    vals = [vals]
                for v in vals:
                    q_parts.append('%s=%s' % (k, unicode(v).encode('utf-8')))
            q_parts.sort()
            qs = '&'.join(q_parts)
        else:
            qs = ""

        parts = [
            headers["Accept"],
            headers["x-summon-date"],
            headers["Host"],
            path,
            qs
        ]
        request_id = ("\n".join(parts)) + "\n"
        return request_id
