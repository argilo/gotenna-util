#!/usr/bin/env python3

import argparse
import base64
import secrets

LEVELS = {
    0: 0x3e75,  # NORMAL
    1: 0x7978,  # SUPER
}

MAGIC = b"1v1da4j839310bohdfgm7jq76o7t63dqsjm37s0v0ucs0dnr"[::-1]

parser = argparse.ArgumentParser()
parser.add_argument("--level", type=int, default=1)
parser.add_argument("--app-id", type=int, default=0x3fff)
args = parser.parse_args()

level = "{:04x}".format(LEVELS[args.level])
app_id = "{:04x}".format(args.app_id)

payload = (secrets.token_hex(10) + level + app_id + secrets.token_hex(10)).encode()
xored = bytes(a ^ b for a, b in zip(payload, MAGIC))
print(base64.urlsafe_b64encode(xored).decode())
