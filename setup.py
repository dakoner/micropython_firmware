from setuptools import setup, find_packages


setup(
    name="micropython_firmware_serial",
    version="1.0",
    packages=find_packages("micropython_firmware_serial"),
    scripts=['scripts/micropython-firmware-serial', 'scripts/micropython-firmware-serial-ui']
)
