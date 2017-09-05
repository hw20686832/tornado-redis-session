# tornado-redis-session
Server side session middleware based on redis

### INSTALL
```
pip install tornado-redis-session
```

### USAGE
```python
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import authenticated, Application

from tornado_redis_session import RedisSessionHandler


class LoginHandler(RedisSessionHandler):
    def get(self):
        name = self.get_argument("name")
        self.set_session('user', name)


class IndexHandler(RedisSessionHandler):
    def get_current_user(self):
        return self.get_session('user')

    @authenticated
    def get(self):
        self.write("hello %s" % self.current_user)


def run():
    app = Application(
        [
            (r'/login', LoginHandler),
            (r'/', IndexHandler),
        ],
        login_url='/login',
        cookie_secret='asdsadsadwqd132432rdews',
        debug=True,
        redis={
            'host': 'localhost',
            'db': 9
        }
    )
    http_server = HTTPServer(app)
    http_server.listen(8887)
    IOLoop.instance().start()

if __name__ == '__main__':
    run()
```
