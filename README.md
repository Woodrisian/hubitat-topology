# Hubitat Topology

This was something I wanted so maybe someone else will stumble upon this and want it too. This doesn't seem like the best way to do this but my brain went down this path.

Pre-reqs:
- Install python 3
- Install docker: https://docs.docker.com/engine/install/ubuntu/
- Docker Pull: docker pull minlag/mermaid-cli:latest
- Ready to go

Have a dedicated directory for this and make sure if you run it as a cronjob you include a "cd /to/the/dir && ./runit" so it has that working directory

Should be able to just for initial setup
```
export HUBITAT=YOUR_LOCAL_URL (Include http://)
docker pull minlag/mermaid-cli:latest
chmod +x topology_export.py
```

Try giving it a run:
```
./topology_export.py
```
Did an mmd file and svg file show up? Woohoo!

Now we have those we need to do something with them, for me I just had home assistant (on the OS) scp periodically to the server/computer I ran this one. But I imagine if you had full CLI access on the HA machine you could just do it right from there. Then just stick it in the /config/www directory and it is public for you to reference, boom
