## Introduction

Dibbler Helper - a small python script to update the kernel routing table according to prefix delegation by dibbler.

## Dependencies
1. Python 3
2. Python's ipaddress-library for sanity checks (https://docs.python.org/3/library/ipaddress.html)

## Installation
1. clone this repo or copy dibbler_helper.py to your local filesystem
2. Update dibbler.conf accordingly - for instance:

```
log-level 8
inactive-mode
script "/usr/local/bin/dibbler_helper.py"

iface eth0 {

        class {
                pool 2001:db8:20a0:b111::/64
        }

        pd-class{
                # network        2001:db8:20a0:b180::/57
                # network range  2001:db8:20a0:b180:0000:0000:0000:0000-2001:db8:20a0:b1ff:ffff:ffff:ffff:ffff
                # 8 networks /60

                pd-pool 2001:db8:20a0:b180::/57
                pd-length 60
        }
}
```
## Logging
dibbler helper logs to `/var/log/dibbler/dibbler_helper.log`. Example output:
```
2016-03-14 17:03:59,429 - dibbler_helper - DEBUG - Executing add for fe80::687e:f9ff:fedb:7295 on eth0
2016-03-14 17:03:59,434 - dibbler_helper - DEBUG - Executing: ip -6 route add 2001:db8:20a0:b180::/60 via fe80::687e:f9ff:fedb:7295 dev eth0
2016-03-14 17:04:38,378 - dibbler_helper - DEBUG - Executing delete for fe80::687e:f9ff:fedb:7295 on eth0
2016-03-14 17:04:38,384 - dibbler_helper - DEBUG - Executing: ip -6 route del 2001:db8:20a0:b180::/60
2016-03-14 17:05:51,701 - dibbler_helper - DEBUG - Executing add for fe80::48cc:acff:feb9:7901 on eth0
2016-03-14 17:05:51,709 - dibbler_helper - DEBUG - Executing: ip -6 route add 2001:db8:20a0:b180::/60 via fe80::48cc:acff:feb9:7901 dev eth0
2016-03-14 18:05:51,637 - dibbler_helper - DEBUG - Executing update for fe80::48cc:acff:feb9:7901 on eth0
2016-03-14 18:05:51,638 - dibbler_helper - INFO - Command not implemented: update
```

## Configuration
There is no configuration. Update dibbler_helper.py according to your needs. 

## Note on scalability
This script is not meant for large deployments. Spawning a python process for each and every delegation event generates load.
For larger deployments,  using an IGP and integrating dibbler into it is a way better option.

## Note on testing / stability
Due to dependencies on the operating system and the simplicity, there is no automated testing 

## Disclaimer
Copyright (c) 2016, yanosz
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the author nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL yanosz BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
