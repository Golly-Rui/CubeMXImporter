#!/usr/bin/python

# Copyright (c) 2015 Carmine Noviello
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

version = 0.1

import os
import argparse
import copy
import logging
from lxml import etree

class CubeMXImporter(object):
    """docstring for CubeMXImporter"""
    def __init__(self):
        super(CubeMXImporter, self).__init__()
        
        self.eclipseprojectpath = ""
        self.dryrun = 0
        self.logger = logging.getLogger(__name__)

    def setCubeMXProjectPath(self, path):
        if os.path.exists(os.path.join(path, ".mxproject")):
            self.cubemxprojectpath = path
        else:
            raise InvalidEclipseFolder("The folder '%s' doesn't seem a CubeMX project" % path)
            
    def getCubeMXProjectPath(self):
        return self.cubemxprojectpath
        
    cubeMXProjectPath = property(getCubeMXProjectPath, setCubeMXProjectPath)


    def setEclipseProjectPath(self, path):
        if os.path.exists(os.path.join(path, ".cproject")):
            self.eclipseprojectpath = path
        else:
            raise InvalidEclipseFolder("The folder '%s' doesn't seem an Eclipse project" % path)
            
    def getEclipseProjectPath(self):
        return self.eclipseprojectpath
        
    eclipseProjectPath = property(getEclipseProjectPath, setEclipseProjectPath)
        
    def addCIncludes(self, includes):
        options = self.projectRoot.xpath("//option[@superClass='ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths']")
        for opt in options:
            for inc in includes:
                listOptionValue = copy.deepcopy(opt[0])
                listOptionValue.attrib["value"] = "&quot;%s&quot;" % inc
                opt.append(listOptionValue)
                
    def deleteOriginalEclipseProjectFiles(self):
        """Deletes useless files generated by the GNU ARM Eclipse plugin"""
        
        dirs = ["src", "include", "system/include/cmsis", "system/src/cmsis"]

        for d in dirs:
            for f in os.listdir(os.path.join(self.eclipseprojectpath, d)):
                f = os.path.join(self.eclipseprojectpath, d, f)
                logging.debug("Deleting %s" % f)
                if not self.dryrun:
                    os.unlink(f)

        self.logger.info("Deleted uneeded files generated by GNU Eclipse plugin")
        
    def parseEclipseProjectFile(self):
        projectFile = os.path.join(self.eclipseprojectpath, ".cproject")
        self.projectRoot = etree.fromstring(open(projectFile).read())
        
    def printEclipseProjectFile(self):
        xmlout = etree.tostring(self.projectRoot, pretty_print=True)
        #lxml correctly escapes the "&" to "&amp;", as specified by the XML standard.
        #However, Eclipse expects that the " charachter is espressed as &quot; So,
        #here we replace the "&amp;" with "&" in the final XML file
        xmlout = xmlout.replace("&amp;", "&")
        print xmlout

    def setDryRun(self, dryrun):
        self.dryrun = dryrun
        if(dryrun > 0):
            self.logger.debug("Running in DryRun mode: the Eclipse project will not be modified")
            
class InvalidEclipseFolder(Exception):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import a CubeMX generated project inside an existing Eclipse project generated with the GNU ARM plugin')
    
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                    help='an integer for the accumulator')
    parser.add_argument('-c', '--cubemx-path', type=str, action='store',
                       help='specifies the PATH of the CubeMX project')

    parser.add_argument('-e', '--eclipse-path', type=str, action='store',
                       help='specifies the PATH of the Eclipse project')

    parser.add_argument('-s', '--stm32-family', type=str, action='store',
                       help='specifies the STM32 family')

    parser.add_argument('-v', '--verbose', type=int, action='store',
                       help='Verbose level')

    parser.add_argument('--dryrun', action='store_true', 
                       help="Doesn't perform operations - for debug purpose")

    args = parser.parse_args()

    if args.verbose == 3:
        logging.basicConfig(level=logging.DEBUG)
    if args.verbose == 2:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR )

    cubeImporter =  CubeMXImporter()
    cubeImporter.setDryRun(args.dryrun)
    cubeImporter.eclipseProjectPath = args.eclipse_path
    cubeImporter.cubeMXProjectPath = args.cubemx_path
    cubeImporter.parseEclipseProjectFile()
    cubeImporter.deleteOriginalEclipseProjectFiles()
    # cubeImporter.addCIncludes(["../middlewares/freertos"])
    # cubeImporter.printEclipseProjectFile()