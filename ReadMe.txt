
// TulipCli;

    TulipCli is a command-line interace to use a database as a psuedo-dictionary data structure.
    This is my project for the Sheffield College Digital Skills Bootcamps: Software Developer course.
    Based on CRUD, you can create, read, update and delete items while being able to search by name 
    and/or description.


// Getting Started;

    # Clone the repo and navigate to the root folder
    git clone https://github.com/skytraveller/tulipcli.git
    cd tulipcli

    # [Optional and recommended] Create a virtual enviroment and activate it
    virtualenv venv
    source venv/bin/activate

    # Install requirements
    python3 -m pip install -r requirements.txt

    # Run with the --help command for more options   
    python3 tulipcli -h

    # Read a dictionary object or string and save it to the database
    python3 tulipcli -db results.db -re "{'test': {'description': 'Hello', 'world!': {'Welcome!': {}}}}"

    # Find a nested item by using ',' as a split   
    python3 tulipcli -db results.db -fi test,Hello,world!

    # Search for an item containing 'ome' in the name or description   
    python3 tulipcli -db results.db -se -na ome -de ome

    # Update the name to 'test' and description to 'update' on item 2
    python3 tulipcli -db results.db -na test -ds update -up -ui 2

    # Write item 2 to the console 
    python3 tulipcli -db results.db -wr -ui 2

    # Delete item 2
    python3 tulipcli -db results.db -de -ui 2


// Database;

    The simple wrapper aroung Sqlalchemy has 3 properties and 6 methods; 

        engine - Sqlalchemy engine
        path - The path, defaulting to ":memory:" for an in-memory database
        session - Sqlalchemy session

        Close - Close the database
        Find - Find an item using navigating through children by name
        Getitemsquery - Create a query to retrieve a list of items given the criteria 
        Open - Open a database, at the (optional) path
        Read - Read a dictionary and store it in the database
        Search - Search for an item by it's name and/or description property.


// Items;

    Items are simple, needing only 4 properties and 2 functions;

        uid - A unique identifier
        parent (optional) - The unique identifier of a parent item
        name (optional) - A name or key
        description (optional) - A description or value

        asdict - Returns the item and it's children (optional) as a dictionary
        delete - Deletes the item and it's children (optional) from the database


// Links;

    Python - https://www.python.org/
    Sqlalchemy - https://www.sqlalchemy.org/
    SQLite - https://sqlite.org/index.html


// Tests;

    Delete
    Find
    Search
    Update
    Write


// Todo;

    Create class and seperate function