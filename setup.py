from setuptools import setup, find_packages


setup(name='hadronutils',
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
              "hadron=hadronutils.cli:cli",
          ]
      },
      include_package_data=True,
      packages=find_packages(),
      package_data={
          'hadronutils.': [
              'default.conf',
          ],
          # 'hadron.node': [
          #     'static/css/*.css',
          #     'static/images/*.png',
          #     'static/js/*.js',
          #     'templates/*.html',
          # ],
      },
      zip_safe=False)
