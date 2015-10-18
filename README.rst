liapi
=====

install
-------
.. code-block:: bash

   git clone git@github.com:dincamihai/liwrapper.git
   cd liwrapper
   virtualenv sandbox
   . sandbox/bin/activate
   pip install -r requirements-dev.txt

run tests
---------
.. code-block:: bash

   py.test

task management
---------------

TODO
````
- validate jmx with xml schema
- improve script:
 - handle all errors
- validate json extractor configuration and handle errors
- create separate extractor python package
- establish how data extracted from jmx translates to configuration params

    +----------------+--------------+
    | xml attribute  | config param |
    +================+==============+
    | test_plan_name | name         |
    +----------------+--------------+
    | domain         | url [param]  |
    +----------------+--------------+

DONE
````
- improve extractor to allow accept flexible json extraction instructions
- script creates config (not just scenario)
- handle data extraction errors
- handle scenario creation errors 400 and 401 as an example and use raise_for_status to handle the rest
- handle configuration creation errors using raise_for_status
