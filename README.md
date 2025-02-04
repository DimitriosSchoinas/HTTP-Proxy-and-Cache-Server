# HTTP-Proxy-and-Cache-Server

This assignment is about how web proxy servers work. 1
Generally, when the client makes a request, the request is sent to the web server. The web server
then processes the request and sends back a response message to the requesting client. In order to
improve the performance we create a proxy server between the client and the web server. Now, both
the request message sent by the client and the response message delivered by the web server pass
through the proxy server. In other words, the client requests the objects via the proxy server. The
proxy server will forward the client’s request to the web server. The web server will then generate a
response message and deliver it to the proxy server, which in turn sends it to the client. 
A typical proxy server can include a cache. The proxy will cache the web pages each time the client
makes a particular request for the first time. The basic functionality of caching works as follows.
When the proxy gets a request, it checks if the requested object is cached, and if yes, it returns the
object from the cache, without contacting the server. If the object is not cached, the proxy retrieves
the object from the server, returns it to the client and caches a copy for future requests. In practice,
the proxy server must verify that the cached responses are still valid and that they are the correct
responses to the client's requests. You can read more about caching and how it is handled in HTTP in
RFC 2068..
The assignment has a mandatory part: a very simplified proxy server which only handles GET-requests,
but is able to handle all kinds of objects - not just HTML pages, but also images. Two versions of this
proxy server are requested: one sequencial and another concurrent. There is also an optional part:
adding to the base server the support of caching,
Please note that lots of web sites only accept secure connections through HTTPS. Our proxy does not
support HTTPS. Please test your proxy with sites that reply to requests in HTTP. The site
http.//vps726303.ovh.net/rc2425 is available for testing

Project PDF:

[Lab11_TPC4 (1).pdf](https://github.com/user-attachments/files/18661052/Lab11_TPC4.1.pdf)
