# Twitch Streams Dashboard
Jesse Fredrickson

[Live!](https://jf-streams-dash.herokuapp.com/)

5/19/19

## Motivation
The purpose of this project is to build and maintain a dashboard which visualizes live and historical twitch viewing and streaming trends. An ideal end state of the project would be a visualization dashboard with integrated machine learning to predict upcoming viewing changes.

## Files
**requirements.txt:** the python modules used in this project and deployment.

**Procfile:** info file for heroku on how to deploy the app.

**myapp.py:** app startup code instructions. Uncommend second line if running on local host.

**wrangling_scripts/wrangle_data.py:** python backend data handling scripts.

**myapp/routes.py:** python backend for passing data from wrangling scripts to the front end.

**myapp/templates/index.html:** main and only html page for the dashboard. Uses Plotly and Bootstrap.

**myapp/templates/static/img/:** holds static graphics


## TODO:

- Refactor wrangling script code
- Reconfigure Twitch API calls to be on intervals with data cached, rather than on page load
- Configure data store to hold cached and historical data
- Develop new graphics for historical trends
- Develop machine learning to predict viewership based on current trends!