#!/usr/bin/env python

from setuptools import setup

setup(name='PyTwitchInteract',
      version='1.0.3',
      description='A collection of tools and utilities for easier interaction with Twitch.',
      author='Vilsol',
      author_email='me@vil.so',
      url='https://github.com/Vilsol/PyTwitchInteract',
      packages=[
          "pytwitchinteract",
          "pytwitchinteract.chat",
          "pytwitchinteract.models",
          "pytwitchinteract.utils"
      ],
      )
