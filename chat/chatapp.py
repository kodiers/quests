import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient
import tornado.options

from tornado.escape import json_decode
from tornado.options import define, options

from urllib import parse

from quests.settings import API_KEY, API_URL

define("port", default=8888, help="run on given port", type=int)

# LIST OF CONNECTED CLIENTS
LISTENERS = []


class SendMessageHandler(tornado.websocket.WebSocketHandler):
    """
    Main request handler for websocket connection
    """
    def open(self, chat_id):
        """
        Open connection for websocket.
        Add object (SendMessageHandler) to LISTENERS list and set chat_id property of object.
        Set sender property to None
        :param chat_id: ID of chat room
        :return: None
        """
        self.sender = None
        self.chat_id = chat_id
        LISTENERS.append(self)

    def handle_request(self, response):
        """
        Handle of response from Django API ENDPOINT.
        For each connected client check chat_id, and if chat_id from response,
        then check, that connection isn't closed and send message to client.
        :param response: Htt response from DJANGO API ENDPOINT
        :return: None
        """
        if response.body is not None:
            # Check that response is not empty and decode to JSON
            json_response = json_decode(response.body)
            for listener in LISTENERS:
                if str(json_response['chat'] == listener.chat_id):
                    if 'Error' in json_response:
                        listener.write_message({'Error':'Incorrect user o chat'})
                    elif listener.ws_connection is not None:
                        listener.write_message(response.body)

    def on_message(self, message):
        """
        Recive message from WebSocket client.
        Send async request to DJANGO API ENDPOINT
        :param message: Messaage from client in JSON format
        :return: Http Response
        """
        json_message = json_decode(message)
        self.sender = json_message['sender']
        message_text = json_message['text']
        http_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(
            API_URL,
            method = 'POST',
            body = parse.urlencode({
                "API_KEY": API_KEY,
                "chat": self.chat_id,
                "sender": self.sender,
                "text": message_text
            })
        )
        response = http_client.fetch(request, self.handle_request)
        return response

    def close(self, code=None, reason=None):
        """
        Remove self object, then client connection is closed from LISTENERS list
        :param code:
        :param reason:
        :return:
        """
        LISTENERS.remove(self)

    def check_origin(self, origin):
        """Override to enable support for allowing alternate origins.

        The ``origin`` argument is the value of the ``Origin`` HTTP
        header, the url responsible for initiating this request.  This
        method is not called for clients that do not send this header;
        such requests are always allowed (because all browsers that
        implement WebSockets support this header, and non-browser
        clients do not have the same cross-site security concerns).

        Should return True to accept the request or False to reject it.
        By default, rejects all requests with an origin on a host other
        than this one.

        This is a security protection against cross site scripting attacks on
        browsers, since WebSockets are allowed to bypass the usual same-origin
        policies and don't use CORS headers.

        To accept all cross-origin traffic (which was the default prior to
        Tornado 4.0), simply override this method to always return true::

            def check_origin(self, origin):
                return True

        To allow connections from any subdomain of your site, you might
        do something like::

            def check_origin(self, origin):
                parsed_origin = urllib.parse.urlparse(origin)
                return parsed_origin.netloc.endswith(".mydomain.com")

        .. versionadded:: 4.0

        parsed_origin = urlparse(origin)
        origin = parsed_origin.netloc
        origin = origin.lower()

        host = self.request.headers.get("Host")

        # Check to see that origin matches host directly, including ports
        return origin == host

        FOR DEVELOPING PURPOSES ALWAYS RETURN TRUE
        TODO: rewrite correctly

        """
        return True


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/send_async_message/(?P<chat_id>\d+)/", SendMessageHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



