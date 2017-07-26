from setuptools import setup, find_packages


setup(name='hadronutils',
      install_requires=[
          'werkzeug',
          'gevent>=1.1.0',
          'gunicorn',
      ],
      entry_points={
          "console_scripts": [
              "hadron=hadronutils.main:gen_chain",
          ]
      },
      include_package_data=True,
      packages=find_packages(),
      package_data={
          'hadron': [
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
