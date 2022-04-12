# CSE 412 Group Project - API

Group \#20: Matthew Bulger, Jeffrey Adams, Ellis Osborn, Jerry Che

Before doing anything, run `cd groupproject`.

##IMPORTANT!
For security reasons, `connection.txt` is not checked into Github, because it contains sensitive information (username and password). When cloning this repository, you must create a new file, `connection.txt` on the same level as `.flaskenv`, containing a string like the following (omit the quotes):

"dbname=groupproject user=YOURUSERNAME password=YOURPASSWORD host=localhost port=5432"

Be sure to replace `YOURUSERNAME` and `YOURPASSWORD` with the appropriate values for your system.

To install dependencies:
1. `pip install -e .`

To initialize the database and insert sample data:
1. `chmod a+x setup.sh`
2. `./setup.sh groupproject 5432`
    - The first parameter is the name of the database, and the directory (relative to `$HOME`) the database will be created in.
    - The second parameter is the port the database should start on. Port `5432` is the default, but it can be useful to change if you have multiple databases running, or another port conflict.

To run the API:
1. `cd app`
2. `python3 -m flask run`
    - Flask will automatically hot-reload whenever you save a file, so you can keep this command running in the terminal while you develop, no need to restart.
