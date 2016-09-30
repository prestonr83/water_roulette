from setuptools import setup

setup(name='water_roulette',
      version='0.8.1',
      description='Water Cannon game for the Raspberry Pi',
      url='http://github.com/prestonr83/water_roulette',
      author='Preston Rodriguez',
      author_email='prestonr83@gmail.com',
      packages=['water_roulette'],
      install_requires=['PyAudio','pygame','RPi.GPIO','Wave'],
      include_package_data=True,
      zip_safe=False)