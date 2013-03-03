#!/usr/bin/env python
import os
from distutils.core import setup

execfile(os.path.join('minecraftswitch', 'release.py'))

setup(
    name='MinecraftSwitch',
    version=version,
    description="Manage multiple minecraft environments on OS X",
    author='Nick Murdoch',
    author_email='minecraftswitch' + '@nivan.net',
    url='http://github.org/flexo/minecraftswitch',
    license='MIT',
    packages=['minecraftswitch'],
    scripts=['minecraft-switch'],
)
