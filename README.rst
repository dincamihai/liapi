liapi
=====

install
-------
.. code-block:: bash

   git clone git@github.com:dincamihai/liapi.git
   cd liapi
   virtualenv sandbox
   . sandbox/bin/activate
   pip install -r requirements-dev.txt

run tests
---------
.. code-block:: bash

   LOAD_IMPACT_TOKEN=<token> py.test

task management
---------------

TODO
````
- validate jmx with schema
- handle data extraction errors
- handle scenario creation errors
- handle configuration creation errors
- establish how data extracted from jmx translates to configuration params

    +----------------+--------------+
    | xml attribute  | config param |
    +================+==============+
    | test_plan_name | name         |
    +----------------+--------------+
    | domain         | url [param]  |
    +----------------+--------------+

- improve script:
 - handle all errors


DONE
````
- improve extractor to allow accept flexible json extraction instructions
- script creates config (not just scenario)
