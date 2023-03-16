# Countries Informer Service

Service to get up-to-date information about countries and cities.

## Requirements:

Install the appropriate software:

1. [Docker Desktop](https://www.docker.com).
2. [Git](https://github.com/git-guides/install-git).
3. [PyCharm](https://www.jetbrains.com/ru-ru/pycharm/download) (optional).

## Installation

Clone the repository to your computer:
```bash
git clone https://github.com/MNV/python-course-countries-informer.git
```

1. To configure the application copy `.env.sample` into `.env` file:
    ```shell
    cp .env.sample .env
    ```
   
    This file contains environment variables that will share their values across the application.
    The sample file (`.env.sample`) contains a set of variables with default values. 
    So it can be configured depending on the environment.
2. Write API keys for APILAYER, OPENWEATHER and NEWSAPI in your .env file in these options:
    - API_KEY_APILAYER=
    - API_KEY_OPENWEATHER=
    - API_KEY_NEWSAPI=

3. Build the container using Docker Compose:
    ```shell
    docker compose build
    ```
    This command should be run from the root directory where `Dockerfile` is located.
    You also need to build the docker container again in case if you have updated `requirements.txt`.
   
4. Now it is possible to run the project inside the Docker container:
    ```shell
    docker compose up
    ```
   When containers are up server starts at [http://0.0.0.0:8020](http://0.0.0.0:8020). You can open it in your browser.

5. To run application correctly set up the database using commands:
    Connect to the application Docker-container:
    ```shell
    docker compose exec app bash
    ```
   Apply migrations to create tables in the database:
    ```shell
    ./manage.py migrate
    ```

## Usage

1. To manage the application you can create superuser:
    ```shell
    ./manage.py createsuperuser
    ```
2. Connect to the application Docker-container (if you are outside the container):
    ```shell
    docker compose exec app bash
    ```

## Automation commands

The project contains a special `Makefile` that provides shortcuts for a set of commands:
1. Build the Docker container:
    ```shell
    make build
    ```

2. Generate Sphinx documentation run:
    ```shell
    make docs-html
    ```

3. Autoformat source code:
    ```shell
    make format
    ```

4. Static analysis (linters):
    ```shell
    make lint
    ```

5. Autotests:
    ```shell
    make test
    ```

6. Run autoformat, linters and tests in one command:
    ```shell
    make all
    ```

Run these commands from the source directory where `Makefile` is located.

## Documentation

The project integrated with the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation engine. 
It allows the creation of documentation from source code. 
So the source code should contain docstrings in [reStructuredText](https://docutils.sourceforge.io/rst.html) format.

To create HTML documentation run this command from the source directory where `Makefile` is located:
```shell
make docs-html
```

After generation documentation can be opened from a file `docs/build/html/index.html`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
