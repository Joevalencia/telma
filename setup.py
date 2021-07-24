import setuptools

setuptools.setup(
    name="telma",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="José Valencia Figueroa",                     # Full name of the author
    author_email="manitest99@gmail.com",
    description="This project aims at carrying out some basic life actuarial calculations. The module contains five classes. See intros documentation for more information", 
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    keywords = ['insurance', 'actuarial science', 'life insurance',
                'python', 'spain'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    install_requires=['pandas==0.25.3',
                      'plotly==4.8.1',
                      'requests==2.22.0',
                      'matplotlib==3.2.1',
                      'numpy==1.17.4'])   # Install other dependencies if any
