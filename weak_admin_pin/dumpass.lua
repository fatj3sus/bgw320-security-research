#!/bin/lua
package.cpath = package.cpath .. ";/www/lib/?.so"
local webui = require "lua_webui"
local access_code = sdb.get("system.access-code")
local decrypt_info = sdb.info("decryptinfo", access_code)
print(decrypt_info[1])
