import logging

from distutils import sysconfig
from os.path import join
from vext import open_spec

def add_vext(vext_file):
    """
    Create an entry for 'setup.py': 'data_files' that will
    install a vext
    """
    dest_dir = join(sysconfig.get_python_lib(), 'vext/specs')
    return (dest_dir, [vext_file])


def check_sysdeps(*vext_files):
    """
    Check that imports in 'test_imports' succeed
    otherwise display message in 'install_hints'
    """
    for vext_file in vext_files:
        success = True
        with open(vext_file) as f:
            vext = open_spec(f)
            install_hint = " ".join(vext.get('install_hints', ['System dependencies not found']))
            for m in vext.get('test_import', ''):
                try:
                    if m:
                        __import__(m)
                except ImportError:
                    print(install_hint)
                    success = False
                    break
    return success
