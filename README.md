### Structure

`api` contains modules for interaction with server's API.

`core` represents main functionality of this framework.

`env` contains set of .env files for various servers.

`.env` is a base file for storing environmental variables.

`.gitignore` describes file types and directories that should not be included into Git.

`conftest.py` contains global pytest fixtures.

`pytest.ini` is main configuration file for pytest.

`README.md` - this file.

`requirements.txt` contains list of necessary packages for this framework.


### Requirements

* [Allure](https://docs.qameta.io/allure/#_about) framework
* Python 3.8 or higher
* Packages listed in `requirements.txt`


### Local launch

1. [Install Allure](https://docs.qameta.io/allure/#_installing_a_commandline).

2. Clone ``mechanist`` repository.
   ```commandline
   git clone https://github.com/kolyat/mechanist.git
   cd mechanist
   ```
   
3. Create and activate virtual environment.
   ```commandline
   virtualenv -p /usr/bin/python venv
   source venv/bin/activate
   ```
   
4. Install requirements.
   ```commandline
   pip install -r requirements.txt
   ```

5. Replace default .env with preferred environmental file.
   ```commandline
   cp env/example.env .env
   ```

6. Make sure `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`, `DEVICES` are correct.

7. Run `pytest`.

8. Run `allure serve allure-results` to see the results.
