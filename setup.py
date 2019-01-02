from distutils.core import setup

setup(
    name='softcolor',  # How you named your package folder
    packages=['softcolor'],  # Chose the same as "name"
    version='0.1.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Soft Color Morphology for Image Processing',  # Give a short description about your library
    author='Pedro Bibiloni',  # Type in your name
    author_email='pedro@bibiloni.es',  # Type in your E-Mail
    url='https://github.com/pbibiloni/softcolor',  # Provide either the link to your github or to your website
    download_url='https://github.com/pbibiloni/softcolor/archive/v_01.tar.gz',  # Source code
    keywords=['Soft Color Morphology', 'Mathematical Morphology', 'Aggregation Functions', 'Image Processing'],
    # Keywords that define your package best
    install_requires=[  # All imports
        'numpy',
        'scipy',
        'scikit-image',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
