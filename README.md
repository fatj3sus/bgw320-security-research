# BGW320 Security Research
This repo contains my findings conducting a cyber security audit of the BGW320. These tools and resources are provided for educational and research purposes only. Only uses these tools on devices you have permission to test with.
The vulnerabilities demonstrated in this repository have not been disclosed to the vendor because they were either (1) already patched before discovery, or (2) determined to have limited real-world security impact.
In this repo you will you find the follow:
1. The first public root for the bgw-320 with physical access and minimal required hardware
2. persvation of root through updates, reboot and factory resets
3. Exposure of the admin pin via the root shell
4. Information about small keyspace used for the default admin access pin

## Decrypting BGW320 firmware images
Once you have obtained a root shell on the device, the firmware image decryption keys can be found in the kernels cmdline arguments

## De-obfuscating the config
The device config is stored in ``/etc/config.cfg`` it is stored in an obfuscated form. It can be de-obfuscated and re-obfuscated by using 
[xmlc](https://github.com/up-n-atom/xmlc)

Happy Hacking!
