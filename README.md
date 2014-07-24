pyremotestreamer
================

Take an arbitrary URL source and stream it to a client. Optionally control the
amount of bytes the client can receive.

reason
======

3rd party provides you direct access to content. They charge you for downloading their content.
You want to act as a VAR to a client base using this providers content.
You don't own the hosting machines so using tcp conn track (kernel) is not an option.

usage
=====
See: http://pip.readthedocs.org/en/latest/installing.html

pip install -r requirements.txt
  
python remotestreamer.py

Then visit http://localhost:6547 in your browser and you should see a download start that appears to be from your machine.
