# Voyager
dynamic engineering traveler system



## Architecture
This app uses Python 3.9.2 and Django 4.0.5.

## Setup
### Database
You will need a database of some kind. Initial dev was done with postgres in mind, so there might be some idiosyncracies, but it *should* work with whatever database you choose as long as it is compatible with Django.

### Site secrets
This app uses `python-dotenv` to handle secret keys and other sensitive parameters. When setting up, copy the `.env_sample` template into `.env` (placed in the same directory as the sample) and fill with the appropriate values.

### Database migrations
You need to build/update the database for full functionality:

    python manage.py migrate


### Run the server
The simplest way to run the server at this point is

    python manage.py runserver


