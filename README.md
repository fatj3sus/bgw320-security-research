# BGW320 Security Research
This repo contains my findings conducting a cyber security audit of the BGW320. These tools and resources are provided for educational and research purposes only. Only uses these tools on devices you have permission to test with.
The vulnerabilites shown in this code have not been disclosed to the vendor as they have either already been patched before they where found or they pose no real security implications
In this repo you will you find the follow:
1. The first public root for the bgw-320 with physical access and minimal required hardware
2. persvation of root through updates and reboot
3. Exposure of the admin pin via the root shell
4. information about small keyspace used for the default admin access pin

## Decrypting BGW320 firmware images
Once you have obtained a root shell on the device, the firmware image decryption keys can be found in the kernels cmdline arguments

## De-obfuscating the config
The device config is stored in ``/etc/config.cfg`` it is stored in an obfuscated form. It can be de-obfuscated and re-obfuscated by using 
[xmlc](https://github.com/up-n-atom/xmlc)

## Recovering admin pin with shell access
1. run the built in lua interpreter
2. Load the shared object used by web server into lua and run the following lua commands to recover the admin code
3. ????
4. Profit
Or you can simply run these commands in the lua interepeter
```lua
package.cpath = package.cpath .. ";/www/lib/?.so"
require "lua_webui"
sdb.info("decryptinfo", sdb.get("system.access-code"))[1]
```
