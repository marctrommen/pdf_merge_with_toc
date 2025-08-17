#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging configuration for the application.
This module sets up the logging configuration for the application using a YAML file.
It allows for flexible logging setup, including different log levels and handlers."""

import logging
import logging.config
import yaml

# -----------------------------------------------------------------------------
def setup_logging(config_path="src/logging_config.yaml") -> None:
    """Sets up logging configuration from a YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

# configure Logging by importing this modul
setup_logging()
logger = logging.getLogger("myapp")
logger.info("Logging is configured.")

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    raise RuntimeError("This is a configuration module and should not get run directly")