# Admin pin
The bgw320 is managed on the lan via a webserver on port 80. All of the configuration for the router requires authenitcatoin with a pin printed on the side of the device.
Although this pin can be changed, every device I found on ebay had not changed the default admin pin. The admin pin is always 10 characters , assumed to be random string with the follow possible characters,
`0123456789/\*@=<>#&%?`. This key space is entirley to small, and if a login to the webserver is able to captured, which conviently is possible since by default all of this happens over http, it is possible
to brute force the default password and gain access to the device. All of this is possible because of the use of http, combined with a weak hashing algorithm `md5` and the small defualt key space. In pratice this attack is infeasable,
as this router offers little configuration options, so there isn't much need to update settings, coupled with the fact that an attacker would actually need to be able to capture you http traffic, which isn't very like for most home instaltions. 
Also of course, if someoen is in your home they could simpley read the access off of the back of your rotuer too.
