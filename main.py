#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * main.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
# *
# *  This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License
# * as published by the Free Software Foundation; either version 2
# * of the License, or (at your option) any later version.
# *
# *  This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# *------------------------------------------------------------------
# *
# Import Modules
#import sys
#import platform
import logging
#import getopt
import suds
import ssl
#import time
#import uuid
#import os
#import csv
#import json

#from prettytable import PrettyTable
#from configobj import ConfigObj
#from suds.client import Client
#from suds.cache import NoCache

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Log/' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )

    ssl._create_default_https_context = ssl._create_unverified_context
    element_config_file = None
    logger = logging.getLogger('cisco.cucm.axl')
    logger.setLevel(logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.CRITICAL)
    logging.getLogger('suds.transport').setLevel(logging.CRITICAL)
    logging.getLogger('suds.xsd.schema').setLevel(logging.CRITICAL)
    logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    console.setLevel=logger.setLevel
    logging.getLogger('').addHandler(console)

    logger.info('Estamos usando Python v%s' % (platform.python_version()))

    '''
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical error message')
    '''

    if not parse_command_line(sys.argv):
        logger.error("Error in parsing arguments")
        sys.exit(1)

    logger.info('Se ha seleccionado el cliente: %s' % (cspconfigfile['INFO']['customer'].upper()))
    csp_soap_client = client_soap(element_config_file)
    customer.Customer(logger, csp_soap_client,cspconfigfile)
    logger.info('Se cerrara el programa')
    sys.exit()