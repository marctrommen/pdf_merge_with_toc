#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymupdf
from fpdf import FPDF

import logging
logger = logging.getLogger("myapp.Application")


# -----------------------------------------------------------------------------
class Application:
    """This class is responsible for managing the application lifecycle and 
    coordinating the program's functionality."""


    # -----------------------------------------------------------------------------
    def __init__(self, configuration: dict) -> None:
        """Initialize the Application with the given configuration."""

        if ((configuration is None) or (not isinstance(configuration, dict))):
            logger.error("Invalid configuration provided to Application.")
            raise ValueError("Configuration must be a dictionary.")
        self.data = configuration
        logger.debug("Application initialized with configuration")

    # -----------------------------------------------------------------------------
    def run(self) -> None:
        """Run the main application logic.
        This method serves as the entry point for the application."""
        logger.info("Running the application")

        self._clean_up()
        self._make_images_from_pdf()
        self._create_pdf()

        logger.info("Application run completed successfully")

    # -----------------------------------------------------------------------------
    def _clean_up(self) -> None:
        """Delete all created files in the build folder from previous run before creating new ones.
        Create the build and data directories if they do not exist."""

        logger.debug(f"Cleaning up previous output files in {self.data['BUILD_DIR']}")

        files = os.listdir(self.data["BUILD_DIR"])
        for file_name in files:
            file_path = os.path.join(self.data["BUILD_DIR"], file_name)
            if file_name.endswith(".png") or file_name.endswith(".pdf"):
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        logger.debug(f"Removed existing file: {file_name}")
                    except OSError as error:
                        logger.error(f"Error removing file {file_path}: {error}")
        
        if not os.path.exists(self.data["BUILD_DIR"]):
            try:
                os.makedirs(self.data["BUILD_DIR"])
                logger.debug(f"Created build directory: {self.data['BUILD_DIR']}")
            except OSError as error:
                logger.error(f"Error creating build directory {self.data['BUILD_DIR']}: {error}")
        
        if not os.path.exists(self.data["DATA_DIR"]):
            try:
                os.makedirs(self.data["DATA_DIR"])
                logger.debug(f"Created data directory: {self.data['DATA_DIR']}")

                if not os.path.exists(self.data["PRIVATE_DATA_DIR"]):
                    try:
                        os.makedirs(self.data["PRIVATE_DATA_DIR"])
                        logger.debug(f"Created private data directory: {self.data['PRIVATE_DATA_DIR']}")
                    except OSError as error:
                        logger.error(f"Error creating private data directory {self.data['PRIVATE_DATA_DIR']}: {error}")
            except OSError as error:
                logger.error(f"Error creating data directory {self.data['DATA_DIR']}: {error}")


    # -----------------------------------------------------------------------------
    def _make_images_from_pdf(self) -> None:
        """Convert the PDF files to images.
        https://pymupdf.readthedocs.io/en/latest/recipes-images.html"""

        logger.debug("Converting PDF files to images")

        target_page_num = 2 # Initialize page number as 1 is for toc
        for item in self.data["PDF_DATA"]["file_list_to_merge"]:
            pdf_path = os.path.join(self.data["PRIVATE_DATA_DIR"], item["file_name"])

            if os.path.isfile(pdf_path):
                logger.debug(f"Processing PDF file: {item["file_name"]}")

                doc = pymupdf.open(pdf_path)
                item["target_page_num"] = target_page_num
                for page in doc:
                    pix = page.get_pixmap(dpi=self.data["PDF_DATA"]["resulting_pdf_file_dpi"], alpha=False)
                    file_name = f"page_{target_page_num:03d}.png"
                    if item["target_page_num"] == target_page_num:
                        item["page_file_name"] = file_name
                    image_path = os.path.join(self.data["BUILD_DIR"], file_name)
                    pix.save(image_path)
                    target_page_num += 1
                    logger.debug(f"Saved image {file_name}")


    # -----------------------------------------------------------------------------
    def _create_pdf(self) -> None:
        """Create a PDF file. This method initializes a PDF document and adds pages to it."""
        logger.debug("Creating PDF document")

        # Initialize the PDF document with specified orientation and page size
        self.pdf_document = FPDF(orientation=self.data["PDF_DATA"]["resulting_pdf_file_page_orientation"], 
                                 unit="mm", 
                                 format=self.data["PDF_DATA"]["resulting_pdf_file_page_size"])

        self._generate_toc()
        self._create_pdf_from_images()

        # Add metadata to the PDF
        self.pdf_document.set_title(self.data["PDF_DATA"]["resulting_pdf_file_title"])
        self.pdf_document.set_author(self.data["PDF_DATA"]["resulting_pdf_file_author"])
        self.pdf_document.set_subject(self.data["PDF_DATA"]["resulting_pdf_file_subject"])
        self.pdf_document.set_keywords(self.data["PDF_DATA"]["resulting_pdf_file_buzzwords"])
        self.pdf_document.set_creator(self.data["PDF_DATA"]["resulting_pdf_file_application"])
        
        # Save the resulting PDF
        resulting_pdf_path = os.path.join(self.data["BUILD_DIR"], self.data["PDF_DATA"]["resulting_pdf_file_name"])
        self.pdf_document.output(resulting_pdf_path)
        
        logger.debug(f"PDF created successfully: {resulting_pdf_path}")


    # -----------------------------------------------------------------------------
    def _generate_toc(self) -> None:
        """Generate a table of contents for the PDF document.
        This method creates a clickable TOC on the first page of the PDF."""
        logger.debug("Generating table of contents")

        self.data["PDF_DATA"]["toc"] = {}

        self.pdf_document.add_page()
        self.pdf_document.set_margins(left=20.0, top=20.0, right=20.0)
        page_width = self.pdf_document.w - self.pdf_document.r_margin - self.pdf_document.l_margin
        logger.debug(f"Page width for TOC: {page_width}")


        self.pdf_document.set_font(family="Arial", style="B", size=16)
        self.pdf_document.cell(w=0, h=10, text=self.data["PDF_DATA"]["toc_title"], ln=True, align="C")

        self.pdf_document.ln(10)

        self.pdf_document.set_font("Arial", size=12)

        for item in self.data["PDF_DATA"]["file_list_to_merge"]:
            toc_entry = item["toc_entry"]
            target_page_num = item["target_page_num"]

            # Create a link placeholder with a link_id for the TOC entry 
            # and store it in the toc dictionary to link to the corresponding page later
            # while adding the images to the PDF
            target_link = self.pdf_document.add_link()
            self.data["PDF_DATA"]["toc"][item["page_file_name"]] = target_link

            # Calculate the width of the dots to fill the space between the TOC entry and the page number
            # and create the TOC entry with clickable link
            toc_entry_width = self.pdf_document.get_string_width(toc_entry)
            page_number_width = self.pdf_document.get_string_width(str(target_page_num))
            double_space_width = self.pdf_document.get_string_width("  ")
            dot_width = self.pdf_document.get_string_width(".")
            dots_fill_count = int((page_width - toc_entry_width - double_space_width - page_number_width) / dot_width - 3)
            logger.debug(f"Calculated dots fill count: {dots_fill_count}")
            dots = "." * dots_fill_count

            toc_text = f"{toc_entry} {dots}"
            # make the TOC entry clickable including the dots but not the page number
            self.pdf_document.cell(w=0, h=10, txt=toc_text, ln=0, link=target_link, align="L")
            self.pdf_document.cell(w=0, h=10, txt=str(target_page_num), link=target_link, ln=True, align="R")
            
        self.pdf_document.ln(10)

        self.pdf_document.set_font("Arial", style="I", size=10)
        self.pdf_document.cell(w=0, h=10, txt=self.data["PDF_DATA"]["toc_hint"], ln=True, align="C")

        logger.debug("Table of contents generated successfully")


    # -----------------------------------------------------------------------------
    def _create_pdf_from_images(self) -> None:
        """Create a PDF file from the images generated from the PDF files.
        https://py-pdf.github.io/fpdf2"""
        logger.debug("Creating PDF from images")


        files = os.listdir(self.data["BUILD_DIR"])
        files = sorted(files)
        for file_name in files:
            if file_name.endswith(".png"):
                file_path = os.path.join(self.data["BUILD_DIR"], file_name)
                if os.path.isfile(file_path):
                    self.pdf_document.add_page()
                    if file_name in self.data["PDF_DATA"]["toc"].keys():
                        # set link target for the TOC entry placeholder
                        # if the file is in the TOC and current page is the first page of the pdf document and the target page
                        self.pdf_document.set_link(self.data["PDF_DATA"]["toc"][file_name], page=self.pdf_document.page_no())
                    self.pdf_document.image(file_path, x=0, y=0, w=210, h=297)
                    logger.debug(f"Image {file_name} added to PDF")
