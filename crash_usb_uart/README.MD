# Stack overflow POC
This vulnerability is patched as of 6.33.5, but works on many prior versions
1. Unplug the BGW320
2. plug in a USB to uart adapater to the BGW320 usb port (MUST be a PL2303)
3. plug in the another USB to UART adapater into a linux PC
4. connect the two UART cables together
5. Run ``crash_poc.py`` as root
6. you have now exercised a stack based buffer flow in ``bist_dataport``
7. Enjoy

Requires pyserial