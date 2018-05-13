"""
    Author: Justin Jones
    Date: 11/27/2017

    File: Processing.py
    Version: 0.3

    Written for use with CodeChat. All of this code works independent of communication methods.
    Group: The Kernel
    COSC 4319.01 Fall 2017
"""

import subprocess
import re
import os


class Processor:
    def __init__(self):
        """Initializes and finds all language definitions."""
        self.__languages = []
        self.__funcs = []

        # supported languages are dynamically gathered from func definitions
        funcs = [func for func in dir(self) if callable(getattr(self, func))]
        for func in funcs:
            if 'process' in func:
                self.__funcs.append(func)
                self.__languages.append(re.findall(r"process\_([a-z|A-Z]*)", func)[0])

    def get_languages(self):
        """return languages for outside reference"""
        return self.__languages

    def get_funcs(self):
        """returns all functions for outside reference"""
        return self.__funcs

    def write_file(self, code: str, path='test'):
        r"""
        Given a string of code and a path, will create a file to execute from and return the path to that file.
        :param code: The code to be run.
        :param path: The path to put the code in.
        :return: The path to the output file.
        """
        with open(path, 'w+', newline=os.linesep) as testfile:
            testfile.truncate()
            testfile.writelines(code)
        return path

    def cleanup(self, fpath: str):
        subprocess.Popen('rm -rf *{}*'.format(fpath), shell=True, executable='/bin/bash')

    # *** BEGIN LANGUAGE DEFINITIONS *** #

    """
    func names should be `process_{language} (self, code:str)` or there may be problems with parsing
    preferably all lower case
    ***A sample definition follows:

    def process_language(self, code: str):
        fname = {however you determine file name, if necessary}
        fpath = self.write_file(code, fname)
        output = subprocess.getoutput('compiler or interpreter {}'.format(fpath))
        if 'whatever is indicative of error if compiled' not in output:
            output += subprocess.getoutput('whatever command to run the compiled file {}'.format(fpath))
        self.cleanup(fpath)
        return output
    """

    def process_ada(self, code: str):
        r"""
        Given Ada code, creates file, captures output, and disposes.
        Ada files should have the name of the main procedure, so the first procedure name is used.
        :param code: The code to be executed.
        :return: The output of passed code.
        """
        fname = re.findall(r"procedure\s([a-z|A-Z|0-9]*)", code)[0].lower()
        fpath = self.write_file(code, "".join([fname, '.adb']))
        output = subprocess.getoutput('gnatmake {}'.format(fpath))
        if 'error' not in output:
            output = subprocess.getoutput('./{}'.format(fname))
        self.cleanup(fname)
        return output

    def process_java(self, code: str):
        r"""
        Given Java code, creates file, captures output, and disposes.
        Java files must have the name of the class, so the first class name is used
        :param code: The code to be executed.
        :return: The output of passed code.
        """
        fname = re.findall(r"class\s([a-z|A-Z|0-9]*)", code)[0]
        fpath = self.write_file(code, "".join([fname, '.java']))
        output = subprocess.getoutput('javac {}'.format(fpath))
        if 'error' not in output:
            output += subprocess.getoutput('java {}'.format(fname))
        self.cleanup(fname)
        return output

    def process_python(self, code: str):
        r"""
        Given Python code, creates file, captures output, and disposes.
        :param code: The code to be executed.
        :return: The output of passed code.
        """
        fpath = self.write_file(code, 'tmp')
        output = subprocess.run('python3.6 {}'.format(fpath), shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                timeout=5,
                                universal_newlines=True
                                )
        self.cleanup(fpath)
        # print(output.stdout)
        if output.stdout == "":
            return output.stderr
        return output.stdout

