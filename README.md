## Sample Python Application

This sample application showcases my Python programming skills and demonstrates my approach to writing clear and concise code. While it doesn't connect to servers or the cloud for this demonstration, it provides a well-structured example that can be easily extended or adapted to suit your needs.

## Installation and Usage

Prerequisites:

Python 3.8 or later: Ensure you have Python 3.8 or a newer version installed on your system. You can check this by running python --version in your terminal.
Poetry: This project uses Poetry for dependency management. If you haven't already, install Poetry by following the instructions at <invalid URL removed>.
Running the Application:

Create a virtual environment: It's highly recommended to create a virtual environment to isolate the project's dependencies and avoid conflicts with other system packages. You can activate Poetry's virtual environment with:

Run in shell:
$ poetry shell

Run the application: Once in the virtual environment, execute the application:
$ python main.py

By default, the application will try to bind to port 8050. If this port is already in use, you can optionally specify a different port:
$ python main.py -p <port number>
