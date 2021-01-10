#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# * Software: resumify                                                       *
# * Version:  1.1.1                                                          *
# * License:  MIT License                                                    *
# *                                                                          *
# * Maintainer:  Devansh Soni (sonidev0201@gmail.com)                        *
# ****************************************************************************

from pathlib import Path
import math
import os
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent

class TwoColumnTemplate(FPDF):
    """Two Column resume template"""

    global name_size, heading_size, border_val, underline_heads, bullet
    name_size = 32
    heading_size = 14
    border_val = 0
    underline_heads = 'u'
    bullet = "•"

    def __init__(self):
        super().__init__()
        self.side_y = 36
        self.main_y = 36
        self.ttl_wid = 190
        self.side_wid = 60
        self.side_x = 10
        self.indent_wid = 4
        self.hr_sep_pos = 32
        self.add_page()

        # Add ubuntu fonts
        self.add_font('Ubuntu-LightItalic', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-LightItalic.ttf'), uni=True)
        self.add_font('Ubuntu-Light', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-Light.ttf'), uni=True)
        self.add_font('Ubuntu', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-Regular.ttf'), uni=True)

        # Set fonts
        self.lightFont = 'Ubuntu-Light'
        self.lightItalicFont = 'Ubuntu-LightItalic'
        self.regularFont = 'Ubuntu'

    @property
    def main_x(self):
        return self.side_wid + self.side_x + 10

    @property
    def main_wid(self):
        return self.ttl_wid - self.side_wid - 10

    def updatePosition0(func):
        "A decorator function mainly used to check if the parameters are valid or not. It also updates the cursor position after inserting the given data"

        def update(self, param, *args):
            if not param or len(param) == 0:
                return
            p = func(self, param, *args)
            if p == 1:
                self.main_y = self.get_y()
            elif p == 0:
                self.side_y = self.get_y()
        return update

    def create_head(self, pos, title):
        "Inserts heading to the page"

        self.initPosition(pos)
        self.set_font(self.regularFont, underline_heads, heading_size)
        if pos == 1:
            self.cell(self.main_wid, 12, txt=title.title(), border=border_val, ln=1, align="L")
            self.main_y = self.get_y()
        elif pos == 0:
            self.cell(self.side_wid, 12, txt=title.title(), border=border_val, ln=1, align="L")
            self.side_y = self.get_y()

    def indent(self, h, al="L"):
        "Create an empty cell for indentation"

        self.cell(self.indent_wid, h, txt="", border=border_val, ln=0, align=al)

    def insert_bullet(self, h):
        "Insert a bullet point in the page"

        self.cell(self.indent_wid, h, txt=bullet, border=border_val, ln=0, align="L")

    def initPosition(self, pos):
        "Move the cursor to the appropriate position"

        if pos == 1:
            self.set_xy(self.main_x, self.main_y)
        elif pos == 0:
            self.set_xy(self.side_x, self.side_y)

    def initPositionX(self, pos):
        "Move the cursor to the appropriate X position"

        if pos == 1:
            self.set_x(self.main_x)
        elif pos == 0:
            self.set_x(self.side_x)

    def get_wid(self, pos):
        "Utility function to get the width of the current column"

        if pos == 1:
            return self.main_wid
        elif pos == 0:
            return self.side_wid

    def top_head(self, name, bolds, contact_info):
        "Insert Name and Contact details"

        fname, lname = name[0], name[1]
        self.set_font(self.lightFont, '', name_size)
        if bolds[0]:
            self.set_font(self.regularFont, '', name_size)

        c1w = math.ceil(((self.ttl_wid - self.get_string_width(fname+" "+lname))/2) + self.get_string_width(fname+" ")) - 1
        self.cell(c1w, 13, txt=fname, border=border_val, ln=0, align="R")
        self.cell(1, 13, txt="", border=border_val, ln=0, align="R")

        self.set_font(self.lightFont, '', name_size)
        if bolds[1]:
            self.set_font(self.regularFont, '', name_size)

        self.cell(self.ttl_wid-c1w-1, 13, txt=lname, border=border_val, ln=1, align="L")

        self.set_font(self.regularFont, '', 10)
        self.cell(self.ttl_wid, 5, txt=contact_info, border=border_val, ln=1, align="C")
        self.line(0, self.hr_sep_pos, 210, self.hr_sep_pos);
        self.ln(10)

    @updatePosition0
    def add_links(self, links):
        "Add links to your profiles on Github, LinkedIn, Twitter or your personal website"

        self.set_y(self.hr_sep_pos+0.5)
        ot = self.ttl_wid/3 - 9
        vals = list(links.items())[:6]

        for i in range(0, len(vals), 3):
            for k, v in vals[i:i+2]:
                self.set_font(self.lightFont, '', 10)
                self.cell(self.get_string_width(k+" : "), 4.5, txt=k+": ", border=border_val, ln=0, align="L")
                self.set_font(self.regularFont, '', 10)
                self.cell(ot-self.get_string_width(k+" : "), 4.5, txt=v, border=border_val, ln=0, align="R")
                self.cell(14, 4.5, txt="", border=border_val, ln=0, align="R")

            for k, v in vals[i+2:i+3]:
                self.set_font(self.lightFont, '', 10)
                self.cell(self.get_string_width(k+" : "), 4.5, txt=k+": ", border=border_val, ln=0, align="L")
                self.set_font(self.regularFont, '', 10)
                self.cell(ot-self.get_string_width(k+" : "), 4.5, txt=v, border=border_val, ln=0, align="R")

            self.ln()

        next_sep_pos = self.hr_sep_pos + math.ceil(len(vals)/3)*5

        self.line(0, next_sep_pos, 210, next_sep_pos);
        self.ln(2)
        self.main_y = self.get_y()
        self.side_y = self.get_y()

        return -1

    @updatePosition0
    def add_education(self, education, pos=0):
        "Add Education section"

        self.create_head(pos, "Education")
        for institute, details in education:
            self.initPositionX(pos)
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5)
            self.multi_cell(self.get_wid(pos)-self.indent_wid, 5, txt=institute, border=border_val, align="L")
            self.ln(0.5)

            self.set_font(self.lightFont, '', 10)

            for tl in ["degree", "dates"]:
                self.initPositionX(pos)
                self.indent(4)
                self.multi_cell(self.get_wid(pos)-self.indent_wid, 4, txt=details[tl], border=border_val, align="L")
                self.ln(1)

            if "other_info" in details:
                self.initPositionX(pos)
                self.indent(4.5)
                self.multi_cell(self.get_wid(pos)-self.indent_wid, 4.5, txt=details['other_info'], border=border_val, align="L")

            self.ln(2)
        self.ln(3)

        return pos

    @updatePosition0
    def add_skills(self, skillset, pos=0):
        "Add Skills section"

        self.create_head(pos, "Skills")
        for k, v in skillset.items():
            self.initPositionX(pos)
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(6)
            self.multi_cell(self.get_wid(pos)-self.indent_wid, 6, txt=k, border=border_val, align="L")

            self.initPositionX(pos)
            self.set_font(self.lightFont, '', 10)
            self.indent(5)
            self.multi_cell(self.get_wid(pos)-self.indent_wid, 5, txt=v, border=border_val, align="L")
            self.ln(1)

        self.ln(4)

        return pos

    @updatePosition0
    def add_certifications(self, certs, pos=0):
        "Add Certifications"

        self.create_head(pos, "Certifications")
        self.set_font(self.regularFont, '', 10)
        for k in certs:
            self.initPositionX(pos)
            self.insert_bullet(5)
            self.multi_cell(self.get_wid(pos)-self.indent_wid, 5, txt=k, border=border_val, align="L")
            self.ln(1)

        self.ln(4)

        return pos

    @updatePosition0
    def add_projects(self, projects, pos=1):
        "Add your Projects"

        self.create_head(pos, "Projects")
        for k, v in projects.items():
            self.initPositionX(pos)
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5.5)
            self.cell(self.get_wid(pos)-self.indent_wid-36, 5.5, txt=k, border=border_val, ln=0, align="L")
            self.set_font(self.lightItalicFont, '', 10)
            self.cell(36, 5.5, txt=v[0], border=border_val, ln=1, align="R")
            self.set_font(self.lightFont, '', 10)

            for x in v[1:]:
                self.initPositionX(pos)
                self.indent(4.5)
                self.multi_cell(self.get_wid(pos)-self.indent_wid, 4.5, txt=x, border=border_val, align="L")

            self.ln(2)
        self.ln(3)

        return pos

    @updatePosition0
    def add_work_experience(self, work, pos=1):
        "Add Work Experience"

        self.create_head(pos, "Work Experience")
        for k, v in work:
            self.initPositionX(pos)
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5)
            self.cell(self.get_wid(pos)-self.indent_wid-36, 5, txt=k, border=border_val, ln=0, align="L")
            self.set_font(self.lightItalicFont, '', 10)
            self.cell(36, 5, txt=v[0], border=border_val, ln=1, align="R")

            self.ln(0.5)

            if 'Org' in v[1]:
                self.initPositionX(pos)
                self.set_font(self.regularFont, '', 10)
                self.indent(5)
                self.multi_cell(self.get_wid(pos)-self.indent_wid, 5, txt=v[1]['Org'], border=border_val, align="L")

            if 'Desc' in v[1]:
                self.initPositionX(pos)
                self.set_font(self.lightFont, '', 10)
                self.indent(4.5)
                self.multi_cell(self.get_wid(pos)-self.indent_wid, 4.5, txt=v[1]['Desc'], border=border_val, align="L")

            self.ln(2)
        self.ln(3)

        return pos

    @updatePosition0
    def add_achievements(self, achievements, pos=1):
        "Add Achievements"

        self.create_head(pos, "Achievements")
        self.set_font(self.regularFont, '', 10)
        for k in achievements:
            self.initPositionX(pos)
            self.insert_bullet(5)
            self.multi_cell(self.get_wid(pos)-self.indent_wid, 5, txt=k, border=border_val, align="L")
            self.ln(.5)

        self.ln(4)

        return pos

    @updatePosition0
    def add_interests(self, interests, pos=1):
        "Add your Interests"

        self.create_head(pos, "Interests")
        self.initPositionX(pos)
        self.set_font(self.lightFont, '', 10)
        self.multi_cell(self.get_wid(pos), 5, txt=", ".join(interests), border=border_val, align="L")
        self.ln(4)

        return pos

    def save(self, filepath):
        "Save your resume"

        try:
            self.output(filepath)
        except:
            print("Can't create PDF file.")

class SingleColumnTemplate(FPDF):
    """Single Column Resume Template"""
    global name_size, heading_size, border_val, underline_heads, bullet, heading_height
    name_size = 32
    heading_size = 14
    heading_height = 11
    border_val = 0
    underline_heads = 'u'
    bullet = "•"

    def __init__(self):
        super().__init__()
        self.main_y = 36
        self.ttl_wid = 190
        self.main_wid = self.ttl_wid
        self.hr_sep_pos = 32
        self.indent_wid = 4
        self.add_page()

        # Add fonts
        self.add_font('Ubuntu-LightItalic', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-LightItalic.ttf'), uni=True)
        self.add_font('Ubuntu-Light', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-Light.ttf'), uni=True)
        self.add_font('Ubuntu', '', os.path.join(BASE_DIR, 'resumify/fonts/Ubuntu/Ubuntu-Regular.ttf'), uni=True)

        # Set fonts
        self.lightFont = 'Ubuntu-Light'
        self.lightItalicFont = 'Ubuntu-LightItalic'
        self.regularFont = 'Ubuntu'

    def updatePosition1(func):
        "A decorator function used to check if the parameters are valid or not"

        def update(self, param, *args):
            if not param or len(param) == 0:
                return
            func(self, param)
        return update

    def create_head(self, title):
        "Inserts heading to the page"

        self.set_font(self.regularFont, underline_heads, heading_size)
        self.cell(self.main_wid, heading_height, txt=title.title(), border=border_val, ln=1, align="L")
        self.main_y = self.get_y()

    def indent(self, h, al="L"):
        "Create an empty cell for indentation"

        self.cell(self.indent_wid, h, txt="", border=border_val, ln=0, align=al)

    def insert_bullet(self, h):
        "Insert a bullet point in the page"

        self.cell(self.indent_wid, h, txt=bullet, border=border_val, ln=0, align="L")

    def top_head(self, name, bolds, contact_info):
        "Insert Name and Contact details"

        fname, lname = name[0], name[1]
        self.set_font(self.lightFont, '', name_size)
        if bolds[0]:
            self.set_font(self.regularFont, '', name_size)

        c1w = math.ceil(((self.ttl_wid - self.get_string_width(fname+" "+lname))/2) + self.get_string_width(fname+" ")) - 1
        self.cell(c1w, 13, txt=fname, border=border_val, ln=0, align="R")
        self.cell(1, 13, txt="", border=border_val, ln=0, align="R")

        self.set_font(self.lightFont, '', name_size)
        if bolds[1]:
            self.set_font(self.regularFont, '', name_size)

        self.cell(self.ttl_wid-c1w-1, 13, txt=lname, border=border_val, ln=1, align="L")

        self.set_font(self.regularFont, '', 10)
        self.cell(self.ttl_wid, 5, txt=contact_info, border=border_val, ln=1, align="C")
        self.line(0, self.hr_sep_pos, 210, self.hr_sep_pos);
        self.ln(8)

    @updatePosition1
    def add_links(self, links):
        "Add links to your profiles on Github, LinkedIn, Twitter or your personal website"

        self.set_y(self.hr_sep_pos+0.5)
        ot = self.main_wid/3 - 9
        vals = list(links.items())

        for i in range(0, len(vals), 3):
            for k, v in vals[i:i+2]:
                self.set_font(self.lightFont, '', 10)
                self.cell(self.get_string_width(k+" : "), 4.5, txt=k+": ", border=border_val, ln=0, align="L")
                self.set_font(self.regularFont, '', 10)
                self.cell(ot-self.get_string_width(k+" : "), 4.5, txt=v, border=border_val, ln=0, align="R")
                self.cell(14, 4.5, txt="", border=border_val, ln=0, align="R")

            for k, v in vals[i+2:i+3]:
                self.set_font(self.lightFont, '', 10)
                self.cell(self.get_string_width(k+" : "), 4.5, txt=k+": ", border=border_val, ln=0, align="L")
                self.set_font(self.regularFont, '', 10)
                self.cell(ot-self.get_string_width(k+" : "), 4.5, txt=v, border=border_val, ln=0, align="R")

            self.ln()

        next_sep_pos = self.hr_sep_pos + math.ceil(len(vals)/3)*5

        self.line(0, next_sep_pos, 210, next_sep_pos);
        self.ln(2)

    @updatePosition1
    def add_education(self, education):
        "Add Education details"

        self.create_head("Education")
        for institute, details in education:
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5)
            self.cell(self.main_wid-self.indent_wid-20, 5, txt=institute, border=border_val, ln=0, align="L")

            self.set_font(self.lightFont, '', 10)
            self.cell(20, 5, txt=details["dates"], border=border_val, ln=1, align="L")
            self.indent(4.5)
            self.multi_cell(self.main_wid-self.indent_wid, 4.5, txt=details["degree"], border=border_val, align="L")

            if "other_info" in details:
                self.indent(4.5)
                self.multi_cell(self.main_wid-self.indent_wid, 4.5, txt=details['other_info'], border=border_val, align="L")

            self.ln(2)
        self.ln(1)

    @updatePosition1
    def add_skills(self, skillset):
        "Add Skills section"

        self.create_head("Skills")
        for k, v in skillset.items():
            self.set_font(self.regularFont, '', 10)
            self.insert_bullet(5)
            self.cell((self.main_wid)*.3-self.indent_wid, 5, txt=k, border=border_val, ln=0, align="L")

            self.set_font(self.lightFont, '', 10)
            self.multi_cell((self.main_wid)*.7, 5, txt=v, border=border_val, align="R")

        self.ln(3)

    @updatePosition1
    def add_projects(self, projects):
        "Add your Projects"

        self.create_head("Projects")
        for k, v in projects.items():
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5)
            self.cell(self.main_wid-self.indent_wid-36, 5, txt=k, border=border_val, ln=0, align="L")

            self.set_font(self.lightItalicFont, '', 10)
            self.cell(36, 5, txt=v[0], border=border_val, ln=1, align="R")
            self.set_font(self.lightFont, '', 10)

            for x in v[1:]:
                self.indent(4.5)
                self.multi_cell(self.main_wid-self.indent_wid, 4.5, txt=x, border=border_val, align="L")

            self.ln(2)
        self.ln(1)

    @updatePosition1
    def add_work_experience(self, work):
        "Add Work Experience"

        self.create_head("Work Experience")
        for k, v in work:
            self.set_font(self.regularFont, '', 11)
            self.insert_bullet(5)
            self.cell(self.main_wid-self.indent_wid-36, 5, txt=k, border=border_val, ln=0, align="L")
            self.set_font(self.lightItalicFont, '', 10)
            self.cell(36, 5, txt=v[0], border=border_val, ln=1, align="R")

            if 'Org' in v[1]:
                self.set_font(self.regularFont, '', 10)
                self.indent(5)
                self.multi_cell(self.main_wid-self.indent_wid, 5, txt=v[1]['Org'], border=border_val, align="L")

            if 'Desc' in v[1]:
                self.set_font(self.lightFont, '', 10)
                self.indent(4.5)
                self.multi_cell(self.main_wid-self.indent_wid, 4.5, txt=v[1]['Desc'], border=border_val, align="L")

            self.ln(2)
        self.ln(1)

    @updatePosition1
    def add_certifications(self, certs):
        "Add Certifications"

        self.create_head("Certifications")
        self.set_font(self.regularFont, '', 10)
        for k in certs:
            self.insert_bullet(5)
            self.multi_cell(self.main_wid-self.indent_wid, 5, txt=k, border=border_val, align="L")

        self.ln(3)

    @updatePosition1
    def add_achievements(self, achievements):
        "Add Achievements"

        self.create_head("Achievements")
        self.set_font(self.regularFont, '', 10)
        for k in achievements:
            self.insert_bullet(5)
            self.multi_cell(self.main_wid-self.indent_wid, 5, txt=k, border=border_val, align="L")

        self.ln(3)

    @updatePosition1
    def add_interests(self, interests):
        "Add your Interests"

        self.create_head("Interests")
        self.set_font(self.lightFont, '', 10)
        self.multi_cell(self.main_wid, 5, txt=", ".join(interests), border=border_val, align="L")
        self.ln(3)

    def save(self, filepath):
        "Save your resume"

        try:
            self.output(filepath)
        except:
            print("Can't create PDF file.")
