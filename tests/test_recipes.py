
'''
test_recipes.py: Ensure all included recipes have proper tags,
                 files, and that app sections are correctly formatted.
Copyright (c) 2017, Vanessa Sochat. All rights reserved.
'''

import os
import re
import sys
import yaml
from fnmatch import fnmatch
from datetime import datetime
try:
    from defaults import Header, Sections
except:
    from .defaults import Header, Sections


from unittest import TestCase


class TestShell(TestCase):

    def setUp(self):
        self.base = '_apps'
        print("---------------------------------------------")

    def tearDown(self):
        print("---------------------------------------------")

    def get_header(self,content):
        '''get the full yaml header from a fullpath (md) file
           content that has already been read from file
        '''
        header = re.findall('---(?s)(.*)---',content)
        self.assertTrue(header != None)
        return yaml.load(header[0])


    def get_recipe(self,content,uri):
        ''' extract a dictionary with key as different app sections
        for a particular recipe. Test as we go
        '''
        recipe = re.findall('```(?s)(.*)```',content)
        self.assertTrue(len(recipe) > 0)
        lines = recipe[0].split('\n')
        sections = dict()
        current_section = None
        commands = []
        for line in lines:
            
            # Start of new section
            if line.startswith('%app'):
                if current_section is not None:
                    sections[current_section] = commands
                    commands = []
                
                current_section = line.split(' ')[0]

                # Add the header name as first in commands
                appname = ''.join(line.split(' ')[1:]).split('#')[0].strip()
                commands.append(appname)
                if current_section in sections:
                    message = "Warning: repeated section %s found" %current_section
                    self.message(uri,message)
                self.assertTrue(current_section not in sections)

            # Continuation of old section, or irrelevant
            else:
                if current_section is not None:
                    command = line.strip()
                    if command not in ['',None]:
                        commands.append(command)

        # Add the last section
        if current_section not in sections:
            sections[current_section] = commands
        return sections


    def message(self,uri,message):
        print('\n**********************************************')
        print(uri + ':')
        print(message)


    def test_recipes(self):
        '''ensure recipes have allowed content, matching with app uri
        '''
        print("Testing SingularityApp Recipes")

        apps = self.find_apps(quiet=False)
        print("Allowed headers are in:\n\n%s" %'\n'.join(Header.allowed))

        for uri, fullpath in apps.items():

            appname = os.path.basename(uri)
            with open(fullpath,'r') as filey:
                content = filey.read()

            # Dictionary of command (eg appname) by lines of content
            sections = self.get_recipe(content,uri)
            for section, commands in sections.items():

                # The first line must always be the correct app name
                # This is the name of the markdown file
                name = commands.pop(0)
                if name != appname:
                    message = 'Name of section %s %s must correspond with file name %s' % (section, name, appname)
                    self.message(uri,message)
                self.assertEqual(name,appname)

        
    def test_metadata(self):
        '''ensure found apps have metadata
        '''
        print("Testing SingularityApp Metadata")

        apps = self.find_apps()
        print("Allowed headers are in:\n\n%s" %'\n'.join(Header.allowed))

        for uri, fullpath in apps.items():
            with open(fullpath,'r') as filey:
                content = filey.read()
            header = self.get_header(content)

            # Make sure that fullpath corresponds with appname - the entire
            # previous path before base must be represented in uri
            filename = os.path.basename(uri)
            uri_test = '-'.join(uri.split('/')[:-1])
            uri_path = '/'.join(uri.split('/')[:-1])
            if uri_test not in filename:
                message = '''Markdown must reflect folders above it. Found:
                             FILENAME: %s.md
                             FOLDERS: %s''' %(filename, uri_path)
                self.message(uri,message)

            self.assertTrue(uri_test in filename)

            # Check that no fields are empty
            for key,val in header.items():
                self.assertTrue(key not in ['', None])
                self.assertTrue(val not in ['', None])

            # Check fields are within allowed
            for field in header.keys():
                if field not in Header.allowed:
                    message ='%s is not an allowed field.' % field
                    self.message(uri,message)

                self.assertTrue(field in Header.allowed)

            # Check that required are present
            [self.assertTrue(x in header) for x in Header.required]

            # Check is datetime, meaning it was formatted correctly
            self.assertTrue(isinstance(header['date'], datetime))            
 
            # Check that one tag at least is os
            found = False
            for tag in header['tags']:
                if tag in Header.oses:
                    found = True
            if found is False:
                message = 'You are required to include at least on OS as a tag, or use "linux" to say any linux OS.'
                self.message(uri,message)
            self.assertTrue(found)

            # If files are included, the folder must correspond to the
            # markdown file name
            if "files" in header:
                app_folder = os.path.basename(fullpath).replace('.md','')
                app_fullpath = "%s/%s" % (os.path.dirname(fullpath), app_folder)
                if not os.path.exists(app_fullpath):
                    print("%s has files present, but folder %s is missing." %(uri, app_fullpath))
                self.assertTrue(os.path.exists(app_fullpath))  
 
                # Check that files are present
                for filey in header['files']:
                    file_fullpath = "%s/%s" %(app_fullpath,filey)
                    if not os.path.exists(file_fullpath):
                        print('File %s specified for uri, but not found in %s' %(filey, app_fullpath))
                    self.assertTrue(os.path.exists(file_fullpath))  
                  

    def find_apps(self, pattern="*.md", quiet=True):
        ''' traverse root directory, and 
        find markdown files to indicate a sci-f app
        '''
        apps = dict()
        for root, dirs, files in os.walk(self.base):
            for filey in files:
                if fnmatch(filey,pattern):
                    fullpath = "%s/%s" %(root, filey)
                    uri = fullpath.strip(self.base).strip('.md').strip('/')
                    apps[uri] = fullpath
                    if quiet is False:
                        print("Found SingularityApp %s" % uri)  
        return apps




if __name__ == '__main__':
    unittest.main()
