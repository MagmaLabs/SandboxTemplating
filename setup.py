import os
from setuptools import setup, find_packages

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "SandboxTemplating",
	version = "0.0.1",
	author = "Theo Julienne",
	author_email = "theo@magmalabs.com.au",
	description = ("A flexible templating library using a real language grammer and AST visitors."),
	license = "MIT",
	keywords = "templating",
	url = "",
	packages=find_packages(),
	long_description=read('README'),
	classifiers=[
		"Development Status :: 3 - Alpha",
		"License :: OSI Approved :: MIT License",
	],
	install_requires=[
		'MarkupSafe',
		'PythonInterfaces',
		'parcon',
	]
)
