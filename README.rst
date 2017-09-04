requests-threads 🎭
===================

This repo contains a Requests session that returns awaitable Twisted
Deferreds instead of Response objects.

It's awesome, basically — check it out:

Examples
--------

Example Usage (using ``async``/``await``):

.. code:: python

	from requests_threads import AsyncSession

	session = AsyncSession()

	async def _main():
	    rs = []
	    for _ in range(100):
	        rs.append(await session.get('http://httpbin.org/get'))
	    print(rs)

	if __name__ == '__main__':
	    session.run(_main)

*This example works on Python 3 only.*

Example Usage (using Twisted):

.. code:: python

	from twisted.internet.defer import inlineCallbacks
	from twisted.internet.task import react
	import requests

	session = requests.AsyncSession()

	@inlineCallbacks
	def main(reactor):
	    responses = []
	    for i in range(100):
	        responses.append(session.get('http://httpbin.org/get'))

	    for response in responses:
	        r = yield response
	        print(r)

	if __name__ == '__main__':
	    react(main)

*This example works on Python 2 and Python 3.*

--------------------

Each request is sent via a new thread, automatically. This works fine for basic
use cases.

**This is a an experiment**, and a preview of the true asyncronous API we have panned for Requests
that is currently *in the works*, but requires a lot of development time. If you'd like to help (p.s. **we need help**, `send me an email <mailto:me@kennethreitz.org>`_).

This API is likely to change, over time, slightly.

Installation
------------

::

    $ pipenv install requests-threads
    ✨🍰✨
