# Dancing and Adjudication Network for Crossing Evaluation (DANCE) System

Web based adjudication system for Ballroom competitions.

## Installation (Ubuntu or Raspbian)
### Preparations
Before installing, make sure you have a domain available.

### Installing the application
Install the application through git:

    git clone https://github.com/AlenAlic/DANCE
    cd DANCE

### Variables
Before installing anything, set the following environment variables:

    export FLASK_APP=run.py
    export DOMAIN=<domain_url>
    export DB_USER=<username>
    export DB_PASSWORD=$(python3 -c "import uuid; print(uuid.uuid4().hex)")
    export SECRET_KEY=$(python3 -c "import uuid; print(uuid.uuid4().hex)")

### Installation script

#### Base items
To install all the base dependencies, run the `install_base` script.

    source scripts/install_base

Then, run the `install_DANCE` script:

    source scripts/install_DANCE
Finally, copy the `DB_PASSWORD` and run the following command to create a login path for backups:

    sudo mysql_config_editor set --login-path=$DB_USER --host=localhost --user=$DB_USER --password
When prompted, paste the password and press Enter.



#### Set up admin account for website
Before you can log in to the site, you will need to create the admin account (and floor manager account) through the shell:

    source venv/bin/activate
    flask shell
    create_tournament_office(tournament_office_password, floor_manager_password, presenter_password)
    exit()
You can log in with the usernames admin, floor, and presenter as the tournament office manager, floor manager, and presenter respectively.

Remember to deactivate the venv:

    deactivate
    