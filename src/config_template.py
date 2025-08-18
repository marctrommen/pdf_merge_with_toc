#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Configuration module for the application.
This module contains the global configuration for the application.
It sets up the project directories, files and other constants.
It also initializes the logging and locale settings.
This configuration is used throughout the application to ensure consistent settings."""

import os


import logging
logger = logging.getLogger("myapp.configuration")

# -----------------------------------------------------------------------------
def configuration() -> dict:
    """Global configuration of the application.
    The configuration is stored in a dictionary which is returned by the function.
    It contains various settings such as project directories, file paths, 
    and other constants."""

    logger.debug("global configuration started")
    config = {}
    
    # Set up project directories
    aPath = os.path.realpath(__file__)
    aPath = os.path.dirname(aPath)
    aPath = os.path.normpath(aPath)
    aPath = os.path.join(aPath, "..")
    aPath = os.path.normpath(aPath)

    # Define the absolute paths for the project directories
    config["PROJECT_ROOT_DIR"] = aPath
    config["SRC_DIR"] = os.path.join( config["PROJECT_ROOT_DIR"], "src" )
    config["DATA_DIR"] = os.path.join( config["PROJECT_ROOT_DIR"], "data" )
    config["PRIVATE_DATA_DIR"] = os.path.join( config["DATA_DIR"], "private" )
    config["BUILD_DIR"] = os.path.join( config["PROJECT_ROOT_DIR"], "build" )
    config["TEST_DIR"] = os.path.join( config["PROJECT_ROOT_DIR"], "test" )

    config["PDF_DATA"] = {
        "resulting_pdf_file_name" : "resulting_file.pdf",
        "resulting_pdf_file_dpi" : 92,
        "resulting_pdf_file_page_size" : "A4",
        "resulting_pdf_file_page_orientation" : "portrait",
        "resulting_pdf_file_title" : "the title of the resulting PDF",
        "resulting_pdf_file_author" : "author name of the resulting PDF",
        "resulting_pdf_file_subject" : "subject of the resulting PDF",
        "resulting_pdf_file_buzzwords" : "pdf_merge_with_toc python",
        "resulting_pdf_file_application" : "pdf_merge_with_toc",
        "toc_title" : "Table of Contents",
        "toc_hint" : "Please, click on the toc entries for jumping to the related page inside this document.",
        "file_list_to_merge" : [
            {
                "file_name" : "file_1_to_add.pdf",
                "toc_entry" : "toc entry for the file to add"
            },
            {
                "file_name" : "file_2_to_add.pdf",
                "toc_entry" : "toc entry for the file to add"
            }
        ]
    }

    logger.debug("global configuration done")
    return config

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    raise RuntimeError("This is a configuration module and should not get run directly")
