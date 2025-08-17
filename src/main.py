#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main entry point for the pdf_merge_with_toc application.
This script initializes the application, sets up logging, and runs the main function.

This application merges multiple PDF files into a single document. The resulting file 
includes a table of contents on the first page, with clickable links to the 
corresponding sections.
"""

import config


from app import Application
import logging
from logging_config import setup_logging
setup_logging()

logger = logging.getLogger("myapp")


# -----------------------------------------------------------------------------
def main() -> None:
    """This main function initializes the application configuration, 
    sets up logging. It serves as a wrapper for the application.
    
    The principle of IOC (Inversion of Control) is used to inject dependencies
    into the Application class."""

    configuration = config.configuration()
    application = Application(configuration=configuration)
    application.run()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    logger.info("Application started.")
    main()
