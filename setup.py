from distutils.core import setup
import py2exe

setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "bundle_files": 1}},
    zipfile = None,
    version = "1.0",
    description = "Convert PDF to HTML",
    name = "pdf2tag",

    console = ["pdf2tag.py"],
    )
