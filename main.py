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
import sys
import platform
import logging
import getopt
import suds
import ssl
import time
import uuid
import os
import csv
import json

from prettytable import PrettyTable
from configobj import ConfigObj
from suds.client import Client
from suds.cache import NoCache
