from setuptools import setup, Command

class PyTest(Command):
    """
    A command to convince setuptools to run pytests.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        pytest.main("test.py")

setup(
    name = 'summoner',
    version = '0.0.2',
    url = 'http://github.com/edsu/summoner',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['summoner',],
    description = 'Work with the Serials Solutions Summon API',
    cmdclass = {'test': PyTest},
    install_requires = ['requests'],
    tests_require=['pytest']
)
