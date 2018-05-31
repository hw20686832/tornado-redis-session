from setuptools import setup


setup(
    name='tornado-redis-session',
    packages=['tornado_redis_session'],
    version='0.1.2',
    description='Server side session middleware based on redis',
    author='David Wong',
    author_email='stef-hw@163.com',
    url='https://github.com/hw20686832/tornado-redis-session',
    #download_url='https://github.com/hw20686832/tornado-redis-session/archive/0.1.1.tar.gz',
    keywords=['tornado', 'session', 'redis'],
    install_requires=['redis', 'tornado'],
    classifiers=[],
)
