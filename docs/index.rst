``stac-validator`` documentation
################################

``stac-validator`` is a library and cli tool for validating `SpatioTemporal Asset Catalogs (STAC) <https://stacspec.org/>`_. It is written in Python and can be used to validate STAC Items, Collections, and Catalogs.  

``stac-validator`` was first developed by `Sparkgeo <https://sparkgeo.com/>`_. It later received support from the `Radiant Earth Foundation <https://radiant.earth/>`_ as part of the work done for `stac-check <https://github.com/stac-utils/stac-check/>`_, which uses the ``stac-validator`` library and adds linting functionality. The ``stac-validator`` CLI tool offers more validation options compared to stac-check. Recent development on ``stac-validator`` has been supported by `Sparkgeo <https://sparkgeo.com/>`_ as well as other open-source contributors. 

Installation
------------

``stac-validator`` can be installed from PyPI:        

.. code-block:: bash

   $ pip install stac-validator      

CLI Usage
---------

``stac-validator`` can be used as a library or as a command line tool.

.. code-block:: shell

   $ stac-validator --help

   Usage: stac-validator [OPTIONS] STAC_FILE

   The `stac-validator` command line tool. Validates a STAC
   file against the STAC specification and prints the validation results to the
   console.

   Args:
      stac_file (str): Path to the STAC file to be validated.
      item_collection (bool): Whether to validate item collection responses.
      pages (int): Maximum number of pages to validate via `item_collection`.
      recursive (bool): Whether to recursively validate all related STAC objects.
      max_depth (int): Maximum depth to traverse when recursing.
      core (bool): Whether to validate core STAC objects only.
      extensions (bool): Whether to validate extensions only.
      links (bool): Whether to additionally validate links. Only works with default mode.
      assets (bool): Whether to additionally validate assets. Only works with default mode.
      custom (str): Path to a custom schema file to validate against.
      verbose (bool): Whether to enable verbose output for recursive mode.
      no_output (bool): Whether to print output to console.
      log_file (str): Path to a log file to save full recursive output.

   Returns:     
      None

   Raises:     
      SystemExit: Exits the program with a status code of 0 if the STAC file is valid, or 1 if it is invalid.

   Options:
      --core                   Validate core stac object only without extensions.
      --extensions             Validate extensions only.
      --links                  Additionally validate links. Only works with default mode.
      --assets                 Additionally validate assets. Only works with default mode.
      -c, --custom TEXT        Validate against a custom schema (local filepath or remote schema).
      -r, --recursive          Recursively validate all related stac objects.
      -m, --max-depth INTEGER  Maximum depth to traverse when recursing. Omit this argument to get full recursion. 
                               Ignored if `recursive == False`.
      --item-collection        Validate item collection response. Can be combined with --pages. Defaults to one page.
      -p, --pages INTEGER      Maximum number of pages to validate via --item-collection. Defaults to one page.
      -v, --verbose            Enables verbose output for recursive mode.
      --no_output              Do not print output to console.
      --log_file TEXT          Save full recursive output to log file (local filepath).
      --version                Show the version and exit.
      --help                   Show this message and exit.

``stac-validator`` can be used to validate local or remotely-hosted STAC objects. The tool will return a list of validation errors if the STAC object is invalid.  

Library
~~~~~~~

``stac-validator`` can be used as a library to validate STAC Items, Collections, and Catalogs. 
It can be used with local or remotely-hosted STAC objects as well as STAC objects represented as a Python dictionary. 
The library will return a list of validation errors if the STAC object is invalid.

Examples
~~~~~~~~

``python dictionary``

.. code-block:: bash
  
   from stac_validator import stac_validator
   
   stac = stac_validator.StacValidate()
   stac.validate_dict(dictionary)
   print(stac.message)

``python item-collection``

.. code-block:: bash

   from stac_validator import stac_validator
   
   stac = stac_validator.StacValidate()
   stac.validate_item_collection_dict(item_collection_dict)
   print(stac.message)


Versions supported
~~~~~~~~~~~~~~~~~~

``stac-validator`` supports the following versions of the STAC specification:

``[0.8.0, 0.8.1, 0.9.0, 1.0.0-beta.1, 1.0.0-beta.2, 1.0.0-rc.1, 1.0.0-rc.2, 1.0.0-rc.3, 1.0.0-rc.4, 1.0.0]``

.. toctree::
   :maxdepth: 1
   
   cli
   utilities
   validator
