#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * main.py
# *------------------------------------------------------------------
# * Cisco AXL Python
# *------------------------------------------------------------------
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
# *  Tenemos que crear una variable global csp_soap_client que sera la
# * que tenga el valor del cliente de SOAP que utilizaremos durante todo
# * el script
# *------------------------------------------------------------------

# Variables Globales:
csp_soap_client = 0

# Import Modules
#import csv
#import getopt
#import json
import logging
import os
import platform
import sys
import suds
import ssl
#import threading
import time
import uuid

# Import SubModules
from prettytable import PrettyTable
from configobj import ConfigObj
from suds.client import Client
from suds.cache import NoCache

def client_soap(config_file):
    # *------------------------------------------------------------------
    # * function client_soap(config_file)
    # *------------------------------------------------------------------
    # *  Esta funcion nos permite crear un cliente de SOAP con los siguientes
    # * datos:
    # *
    # * IP Address
    # * Usuario
    # * Password
    # *------------------------------------------------------------------
    # *

    global csp_soap_client

    logger.debug('Ha entrado en la funcion client_soap()')
    csp_cmserver = cspconfigfile['CUCM']['server']
    csp_ip = cspconfigfile['CUCM']['ip']
    csp_username = cspconfigfile['CUCM']['user']
    csp_password = cspconfigfile['CUCM']['pass']
    csp_version = cspconfigfile['CUCM']['version']

    if platform.system() == 'Windows':
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file:///' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//' + csp_version + '//AXLAPI.wsdl'
    else:
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file:///' + os.getcwd() + '/Schema/CUCM/' + csp_version + '/AXLAPI.wsdl'

    csp_location = 'https://' + csp_cmserver + ':8443/axl/'

    logger.debug('El valor de csp_cmserver es: %s' % (csp_cmserver))
    logger.debug('El valor de csp_ip es: %s' % (csp_ip))
    logger.debug('El valor de csp_username es: %s' % (csp_username))
    logger.debug('El valor de csp_version es: %s' % (csp_version))
    logger.debug('El valor de csp_location es: %s' % (csp_location))
    logger.debug('El valor de wsdl es: %s' % (wsdl))

    # Tiempo de inicio de ejecucion.
    try:
        csp_soap_client = suds.client.Client(wsdl,
                                             location = csp_location,
                                             username = csp_username,
                                             password = csp_password,
                                             cache = NoCache(),
                                             )
    except:
        logger.error('Se ha producido un error al crear el cliente soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha creado el cliente SOAP.')
    try:
        csp_version_long = csp_soap_client.service.getCCMVersion(processNodeName=csp_ip)
    except:
        logger.error('Se ha producido un error al comprobar la version del servidor soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha verificado la version del servidor soap.')
        csp_table = PrettyTable(['Server','Username','Version Conf_File','Version Real'])
        csp_table.add_row([csp_cmserver, csp_username, csp_version,csp_version_long['return']['componentVersion'].version])
        csp_table_response = csp_table.get_string(
            fields=['Server', 'Username', 'Version Conf_File', 'Version Real'], sortby="Server")
        logger.info('\n\n' + csp_table_response + '\n')

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-24s [%(name)s - %(levelname)s] : %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Log/' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )

    ssl._create_default_https_context = ssl._create_unverified_context
    element_config_file = None
    logger = logging.getLogger('cisco.cucm.axl')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('suds.client').setLevel(logging.CRITICAL)
    logging.getLogger('suds.transport').setLevel(logging.CRITICAL)
    logging.getLogger('suds.xsd.schema').setLevel(logging.CRITICAL)
    logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-24s [%(name)s - %(levelname)s] : %(message)s')
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
    
    #if not parse_command_line(sys.argv):
    #    logger.error("Error in parsing arguments")
    #    sys.exit(1)

    # Buscamos los ficheros de configuracion en el directorio conf/
    logger.debug('Buscamos todos los archivos *.cfg del directorio conf/')
    csp_table_file=PrettyTable(['id', 'Filename'])
    csp_table_id=0

    csp_dir='conf/'
    csp_file = []
    for file in os.listdir(csp_dir):
        if file.endswith(".cfg"):
            csp_file.append(file)
            csp_table_file.add_row([csp_table_id,file])
            csp_table_id += 1

    logger.debug('El numero de ficheros de configuracion es: %d' % (csp_table_id))

    if csp_table_id == 1:
        element_config_file = csp_dir + csp_file[0]
        logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
        cspconfigfile = ConfigObj(element_config_file)
    else:
        print (csp_table_file)
        csp_file_config = input('Seleccione el archivo de configuracion: ')
        if int(csp_file_config) > csp_table_id - 1:
            logger.error('Ha seleccionado un fichero erroneo')
            sys.exit()
        else:
            element_config_file = csp_dir + csp_file[int(csp_file_config)]
            logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
            cspconfigfile = ConfigObj(element_config_file)

    logger.info('Se ha seleccionado el cliente: %s' % (cspconfigfile['INFO']['customer'].upper()))
    client_soap(element_config_file)
    #customer.Customer(logger, csp_soap_client,cspconfigfile)
    logger.info('Se cerrara el programa')
    sys.exit()