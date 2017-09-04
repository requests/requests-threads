import inspect

from twisted.internet import threads
from twisted.internet.defer import ensureDeferred
from twisted.internet.error import ReactorAlreadyInstalledError
from twisted.internet import task

from requests import Session


class AsyncSession(Session):
    """An Asyncronous Requests session.

    Provides cookie persistence, connection-pooling, and configuration.

    Basic Usage::

      >>> import requests
      >>> s = requests.Session()
      >>> s.get('http://httpbin.org/get')
      <Response [200]>

    Or as a context manager::

      >>> with requests.Session() as s:
      >>>     s.get('http://httpbin.org/get')
      <Response [200]>
    """

    def __init__(self, n=None, reactor=None, *args, **kwargs):
        if reactor is None:
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                try:
                    from twisted.internet import asyncioreactor
                    asyncioreactor.install(loop)
                except (ReactorAlreadyInstalledError, ImportError):
                    pass
            except ImportError:
                pass

            # Adjust the pool size, according to n.
            if n:
                from twisted.internet import reactor
                pool = reactor.getThreadPool()
                pool.adjustPoolsize(0, n)

        super(AsyncSession, self).__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        """Maintains the existing api for Session.request.
        Used by all of the higher level methods, e.g. Session.get.
        """
        func = super(AsyncSession, self).request
        return threads.deferToThread(func, *args, **kwargs)

    def wrap(self, *args, **kwargs):
        return ensureDeferred(*args, **kwargs)

    def run(self, f):
        # Python 3 only.
        if hasattr(inspect, 'iscoroutinefunction'):
            # Is this a coroutine?
            if inspect.iscoroutinefunction(f):
                def w(reactor):
                    return self.wrap(f())
                # If so, convert coroutine to Deferred automatically.
                return task.react(w)
        else:
            # Otherwise, run the Defferred.
            return task.react(f)
