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
- handle scenario creation errors (use API instead of SDK)
- handle configuration creation errors (use API instead of SDK)
- improve script:
 - handle all errors
- validate json configuration and handle errors
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
