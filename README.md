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

* Windows 7 or higher
* Python 3.8 or higher
* [Allure](https://docs.qameta.io/allure/#_about) framework
* Packages listed in `requirements.txt`


### Installation

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

5. Install webdrivers for [SelenuimBase](https://seleniumbase.io/).
   ```commandline
   seleniumbase get chromedriver
   seleniumbase get geckodriver
   seleniumbase get edgedriver
   ```

6. Replace default .env with preferred environmental file.
   ```commandline
   cp env/example.env .env
   ```

7. Check `.env` vars:
   1. `USER_EMAIL`
   2. `USER_PASSWORD`
   3. `DEVICES`
   4. `CAMPAIGNS`


### Test run

##### Player

`pytest -nauto --dist=loadscope --max-worker-restart=16 test_player/`

`allure serve allure-results`

##### Web UI

`pytest -n0 --reuse-session --dashboard --html=tmp/report.html test_ui/`
