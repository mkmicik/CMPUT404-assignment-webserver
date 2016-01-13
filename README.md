CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

=============================
| 		 Alterations 		|
=============================
Author: 		Mike Kmicik
Date Modified: 	Jan. 11, 2016

Summary
==========
When the server receives a request, it passes the raw request to a helper function. This helper function then parses the resource path out of the request and ensures that the request is valid. In order to be valid, the request must be within the www/ folder (must not contain '..' patterns in the path) and should point to an existing resource. If the path ends in '/', it checks for the existence of an 'index.html' file in the given location. If it exists, it is returned. If none of these cases pass, a '404 Not Found' response is served. Assuming the resource does exist, a HTTP response is build using the correct mime type and is served back to the client. Currently, the server recognizes html, css, and image/x-icon mime types.

Know Issues
==========
There are no known issues with my implementation, all features should function as expected.

Collaboration
=============
I did not collaborate with any other students for this assignment.