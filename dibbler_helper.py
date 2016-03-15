#!/usr/bin/env python3
#Copyright (c) 2016, yanosz
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL yanosz BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import ipaddress
import logging
from os import environ
import subprocess

logger = logging.getLogger('dibbler_helper')
logger.setLevel(logging.DEBUG)

# Adapter for Linux' ip-command
def execute(cmd,iface,peer,prefix):
    # Try to remove routes first - contionue until no route is removed
    cmd_list_remove = ["ip", "-6" , "route", "del", prefix]
    while subprocess.call(cmd_list_remove) == 0:
         logger.debug("Executing: " + " ".join(cmd_list_remove))
    if(cmd == "add"):
        cmd_list = ["ip","-6","route","add", prefix,"via",peer, "dev",iface]                                                                                
        logger.debug("Executing: " + " ".join(cmd_list))                                                                                                    
        subprocess.call(cmd_list)                                                                                                                           
                                                                                                                                                            
def process_route(cmd,iface,peer,prefix):                                                                                                                   
        # Missing parameters?                                                                                                                               
    if cmd not in ["add","delete"] :
        logger.info("Command not implemented: "+cmd)
        return
    # Valid addresses / network?
    try:
        ipaddress.ip_address(peer)
        ipaddress.ip_network(prefix)
    except ValueError:
        logger.error("Malformed network sring data" + peer + " / " + prefix)
        return 
    # Ok, go for it
    execute(cmd,iface,peer,prefix)

def main():
    try:
        if_name = environ['IFACE']
        client = environ['REMOTE_ADDR']
        cmd = sys.argv[1]
        prefix_index = 1
        logger.debug("Executing " +cmd + " for " + client + " on " + if_name)
        while 'PREFIX'+str(prefix_index) in environ:
            prefix = environ['PREFIX'+str(prefix_index)]
            prefix_length = environ['PREFIX'+str(prefix_index)+"LEN"]
            process_route(cmd,if_name, client, prefix + "/" + prefix_length)
            prefix_index += 1
    except KeyError as e:
        logger.error("Missing parameter in environment" + str(e))


if __name__ == "__main__":
    fh = logging.FileHandler('/var/log/dibbler/dibbler_helper.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    main()
