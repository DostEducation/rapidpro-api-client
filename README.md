# rapidpro-api-client

## About
An API to connect with Rapid Pro to update fields or groups by triggering it.

## Installation

### Prerequisite
1. pyenv
2. python 3.8+

### Steps
1. Clone the repository
    ```sh
    git clone https://github.com/DostEducation/rapidpro-api-client.git
    ```
2. Switch to project folder and setup the vertual environment
    ```sh
    cd rapidpro-api-client
    python3 -m venv venv
    ```
3. Activate the virtual environment
    ```sh
    source ./venv/bin/activate  (For Bash)
    ./venv/Scripts/activate   (For Powershell/CMD)
    ```
4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
5. Set up your .env file by copying .env.example
    ```sh
    cp .env.example .env
    ```
6. Add/update variables in your `.env` file for your environment.
7. Run the following command to get started with pre-commit
    ```sh
    pre-commit install
    ```
8. Start the server by following command
    ```sh
    functions_framework --target=trigger --debug
    ```
