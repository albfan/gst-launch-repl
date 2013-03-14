from setuptools import setup, find_packages

setup(
    name='gst-launch-dynamic',
    version='0.1',
    description='Launch a GStreamer pipeline and then control it via stdin.',
    author='Peter Ward',
    author_email='peteraward@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gst-launch-dynamic = gstlaunchdynamic:main',
        ]
    }
)
