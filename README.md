Contents:
------------

- `server.py` - python file for running the TCP proxy server app.
- `Dockerfile` - docker file for dockerizing the proxy server app.
- `multi_server` - folder that includes all the needed for running TCP/UDP proxy server for handling both types of protocols.

How To Run
------------

- you can run the proxy by doing either of these:

  - Build the image with this command `docker build -t [your-image-name] .` and then run it with this command 
  `docker run -d -p 53:53 --name -e DoT_HOST="[your-DoT-host]" [container-name] [your-image-name]`
  the `DoT_HOST` env variable is optional in case you wanna change the default DoT server.

  - If you don't want to build the image I have built the image and pushed it to my own Dockerhub account and made it public so anyone can use it 
  `docker run -d -p 53:53 --name [container-name] bashar1993/dot-proxy-server:1.0`.

  - `python3 server.py` to run without docker.

#### note:

    in all cases you need port 53 to be available on your host

Answers and suggestions
------------

- I used the `ssl` and `socket` python libraries for implementaion, the file `server.py` contains notes for every step.

- security concerns, I think DNS is a very critical part in any environment and it could take down the whole system in case something went wrong like a bug in the code which calls for heavy testing before launching or a DoS attack by one of the services calling the DNS server so we probably need to add some code for blocking a source for a certain amount of time if the server receives a high number of requests from it in a specific period of time.

- for deploying in a microsservice-oriented continarized environment like kubernetes we can run a deployment of multiple replicas and a service resource that load balances across those replicas so all other services can connect to it and all external DNS queries will pass through it and will be TLS secured.

- other improvments, you already mentioned a couple improvments like allowing multiple connections at the same time and allowing UDP requests which I did both in the code, I would also say allowing fallback to UDP on the other side (DoT server side) for higher availability and of course configuring multiple DoT servers.

- `multi_server.py` is the code for a proxy server that handles both TCP/UDP protocols by running a different thread for each, it works with both TCP/UDP clients while still querying TCP on the other side, you can find detailed explanation in the file comments. to run this server, cd into the folder `multi_server` and build the image `docker build -t [your-image-name] .` and then run it `docker run -d -p 53:53/tcp -p 53:53/udp --name [container-name] [your-image-name]` . you can use the image I pushed to my account `bashar1993/dot-multi-server:1.0`.