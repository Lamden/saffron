from setuptools import setup, find_packages


setup(name='saffron',
      packages = ['saffron'],
      version = '0.1',
      description = 'blockchain artifact development tools',
      author = 'Lamden',
      author_email = 'james@lamden.io',
      url = 'https://github.com/Lamden/saffron',
      download_url = 'https://github.com/Lamden/saffron/archive/0.1.tar.gz',
      keywords = ['testing', 'logging', 'cryptocurrency', 'smartcontracts', 'ethereum', 'dashboards'],
      classifiers = [],
      install_requires=[
          'werkzeug',
          'gevent>=1.1.0',
          'gunicorn',
          'web3',
          'jinja2',
          'py-solc',
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
      packages=find_packages(),
      package_data={
          'saffron.': [
              'default.conf',
          ],
          # 'hadron.node': [
          #     'templates/*.html',
          # ],
      },
      zip_safe=False
      )
