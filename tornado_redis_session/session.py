# coding:utf-8
import random
import datetime
from hashlib import sha1

import redis
from tornado.web import RequestHandler


class SessionManager(object):
    def __init__(self, redis):
        self.redis = redis

    def set_session(self, sessionid, identifier, ctx, expires=None):
        self.redis.hset("session:%s" % sessionid, identifier, ctx)
        if expires:
            self.redis.expire("session:%s" % sessionid, int(expires))

    def get_session(self, sessionid, identifier):
        ctx = self.redis.hget("session:%s" % sessionid, identifier)
        return ctx

    def clear(self, sessionid, identifier):
        self.redis.hdel("session:%s" % sessionid, identifier)

    def clear_all(self, sessionid):
        self.redis.delete("session:%s" % sessionid)


class RedisSessionHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RedisSessionHandler, self).__init__(*args, **kwargs)
        _redis = redis.Redis(**self.settings['redis'])
        self.__session_manager = SessionManager(_redis)

    def get_sessionid(self):
        return self.get_cookie('tsessionid')

    def __gen_sessionid(self):
        salt = "-".join((
            str(datetime.datetime.now()),
            str(random.random()),
            self.request.remote_ip,
            self.settings.get("cookie_secret")
        ))
        sessionid = sha1(salt).hexdigest()
        sessionid = "TSESSIONID_%s" % sessionid
        return sessionid

    def get_session(self, key):
        sessionid = self.get_sessionid()
        if sessionid:
            return self.__session_manager.get_session(sessionid, key)

    def set_session(self, key, value):
        sessionid = self.get_sessionid()
        if not sessionid:
            sessionid = self.__gen_sessionid()
            self.set_cookie('tsessionid', sessionid)

        return self.__session_manager.set_session(sessionid, key, value)

    def clear_session(self, key):
        sessionid = self.get_sessionid()
        return self.__session_manager.clear(sessionid, key)

    def clear_all_session(self):
        sessionid = self.get_sessionid()
        return self.__session_manager.clear_all(sessionid)
