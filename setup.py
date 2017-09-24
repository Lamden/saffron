from setuptools import setup, find_packages


setup(name='saffron-cli',
      packages=find_packages(),
      version = '0.1.11',
      description = 'blockchain artifact development tools',
      author = 'Lamden',
      author_email = 'james@lamden.io',
      url = 'https://github.com/Lamden/saffron',
      download_url = 'https://github.com/Lamden/saffron/archive/0.1.tar.gz',
      keywords = ['testing', 'logging', 'cryptocurrency', 'smartcontracts', 'ethereum', 'dashboards'],
      classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Environment :: No Input/Output (Daemon)',
            'Environment :: OpenStack',
            'Intended Audience :: Education',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Version Control :: Git',
            'Topic :: Software Development :: Libraries',
            'Topic :: Education :: Computer Aided Instruction (CAI)',
            'Topic :: Office/Business :: Groupware',
      ],
      install_requires=[
          'werkzeug',
          'gevent>=1.1.0',
          'gunicorn',
          'web3',
          'jinja2',
          'pytest',
          'py-solc',
          'click'
      ],
      entry_points={
          "console_scripts": [
              "saffron=saffron.cli:cli",
          ]
      },
      include_package_data=True,

      package_data={
          'saffron.': [
              'default.conf',
          ],
          # 'saffron.node': [
          #     'templates/*.html',
          # ],
      },
      zip_safe=False
      )
