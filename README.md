
# Green Haven Server

## Client Side Application

https://github.com/rochelle-rossman/green-haven-client

## Project Setup

- Navigate to where you want to clone the repo in your terminal
- Clone Repo on to Local Machine


    ```shell
    git clone git@github.com:rochelle-rossman/green-haven-server.git
    ```

- Open Cloned Project

    ```shell
    cd green-haven-server
    code .
    ```

- Create Virtual Envirunment

    ```shell
    pipenv shell
    ```

- Select interpreter within vscode
<kbd>Shift</kbd> + <kbd>Command</kbd> + <kbd>P</kbd> (Mac)
<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>(Windows/Linux)
    - Open your Command Palette
    - Search for "Python: Select Interpreter"
    - Select the interpreter that includes `green-haven-server` in the name.

- Install Dependencies

    ```shell
    pipenv install
    ```

- Run Migrations

    ```shell
    python manage.py migrate
    ```

- Start Project

    ```shell
    python manage.py runserver
    ```

- View the API

    ```shell
    Performing system checks...

    System check identified no issues (0 silenced).
    March 15, 2023 - 19:25:54
    Django version 4.1.6, using settings 'greenhaven.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    ```




## ERD
[![draw-SQL-green-haven-export-2023-03-13.png](https://i.postimg.cc/BbcvHnMH/draw-SQL-green-haven-export-2023-03-13.png)](https://postimg.cc/n9rZtp8h)
