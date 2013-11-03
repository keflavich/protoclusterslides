#!/usr/bin/env python

import os
import glob
import shutil
import tempfile
import sys

from IPython.nbconvert.nbconvertapp import NbConvertApp

from setuptools import setup, Command
import subprocess


class BuildNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        for arg in range(len(sys.argv[1:])):
            sys.argv.pop(-1)

        # First convert the lecture notes to slides - we have to do them
        # individually in order to be able to specify a custom output prefix for
        # each.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'slides'
        app.config.Exporter.template_file = 'output_toggle.tpl'
        # remote version
        app.config.Exporter.reveal_prefix = "//cdn.jsdelivr.net/reveal.js/2.4.0/"
        # local version
        app.config.Exporter.reveal_prefix = '' # 
        for notebook in glob.glob('*.ipynb'):
            app.notebooks = [notebook]
            app.output_base = notebook.replace('.ipynb', '')
            app.start()

            outfile = "build/{}.slides.html".format(app.output_base)
            if os.path.exists(outfile):
                os.remove(outfile)
            shutil.move(app.output_base+".slides.html",outfile)

        # Now convert the lecture notes, problem sets, and practice problems to
        # HTML notebooks.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'html'
        for notebook in glob.glob('*.ipynb'):
            app.notebooks = [notebook]
            app.output_base = notebook.replace('.ipynb', '')
            app.start()

            outfile = "build/{}.html".format(app.output_base)
            if os.path.exists(outfile):
                os.remove(outfile)
            shutil.move(app.output_base+".html",outfile)


class DeployNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        result1 = subprocess.Popen(['git','clone','git@github.com:hakimel/reveal.js.git','build/reveal.js'])
        result2 = subprocess.Popen(['ghp-import','build/'])
        result3 = subprocess.Popen(['git','push','origin','gh-pages'])
    

class RunNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        # Now convert the lecture notes, problem sets, and practice problems to
        # HTML notebooks.

        from runipy.notebook_runner import NotebookRunner

        start_dir = os.path.abspath('.')

        for notebook in glob.glob('*.ipynb'):
            os.chdir(os.path.dirname(notebook))
            r = NotebookRunner(os.path.basename(notebook))
            r.run_notebook(skip_exceptions=True)
            r.save_notebook(os.path.basename(notebook))
            os.chdir(start_dir)


setup(name='BoundProtoClusters',
      cmdclass={'run':RunNotes, 'build': BuildNotes, 'deploy':DeployNotes})
