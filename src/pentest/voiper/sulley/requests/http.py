from sulley import *

# GET /index.html HTTP/1.1

s_initialize("HTTP BASIC")
s_group("verbs", values=["GET", "HEAD", "POST", "TRACE"])
if s_block_start("body", group="verbs"):
    s_delim(" ")
    s_delim("/")
    s_string("index.html")
    s_delim(" ")
    s_string("HTTP")
    s_delim("/")
    s_string("1")
    s_delim(".")
    s_string("1")
    s_static("\r\n\r\n")
s_block_end()