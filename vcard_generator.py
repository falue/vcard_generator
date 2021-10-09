#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Generates an abitrary number of valid .vcf vCard contacts based on the
parameters set at the beginning of the file. See also:
http://softwareas.com/vcard-for-developers
http://en.wikipedia.org/wiki/VCard
"""

import random, sys

################################## Parameters ##################################

# We'll use this data no matter what the user tells us.

# What fields shall be populated?
target_fields = {"Name":True,
                 "FullName":True,
                 "Organization":True,
                 "Address":True,
                 "Title":True,
                 "Phone":True,
                 "Email":True,}

# Data that we'll use to populate the cards' fields.
first_names = ["Alice", "Bob", "Carol", "David", "Elena", "Farquahd", "Gretel",
               "Hans", "Iris", "Junichi", "Khalisha", "Lee", "Mina", "Nassif",
               "Oba", "Prudha", "Hida", "Kaiu", "Aaron", "Sangamon",
               "Ferdinand", "Sanjay", "Asok"]
last_names = ["Smith", "Jones", "Smythe", "Jorgenson", "Kim", "Luxury-Yacht",
              "Throatwarbler-Mangrove", "Cooper", "Black", "Ahmedinejad",
              "al-Tikriti", "al-Bagram", "von Trapp", "von der Wallenheim",
              "Gamgee", "Proudfoot", "Brewer", "Kagehiro", "Ng",
              "Nguyen", "Salzmann", "Bear", "Powers","Kusanagi", "Dengo",
              "Mukherjee","Balaam"]

# Street numbers will be generated at random.  All addresses are
# situated in Anytown, CA, ZIP 12345, United States of America.

streets = ["Paper Street", "Fictional Lane", "Placid Avenue", "Blank Road",
           "Suspicious Parkway"]

orgs = ["Monty Python's Flying Circus", "Golden Egg Bonus Company, LLC",
        "Dewey Cheatham & Howe, Tax and Family Law", "Improv Everywhere",
        "Owl-Stretching Enthusiasts' Club", "International R. Mutt Fan Club",
        "Paper Street Soap Company", "River City Pool Table Company",
        "Desert Bus Runs", "Impossibilities Inc", "The X-Men"]

titles = ["Mercenary", "Chief Tomfoolery Engineer", "Nonsense Supervisor",
          "Skylark", "Isn't It About Time For Lunch", "Famous Author",
          "Fictional Person", "Space Traveller", "Architect",
          "International Person Of Mystery", "Sith Lord", "Sith Apprentice",
          "Sith Intern", "Archaeologist", "Scout", "Heavy", "Sniper"]

# Phone numbers will be generated in the form 555-NNNN.
# Email addresses will be generated in the form  firstname.lastname@example.com

################################## Actions ###################################

class CardFiller:
    """A class whose instances take the basic dataset we're working with,
    shuffle it, and grind through generating VCard entries based on it. """
    def __init__(self, first_names, last_names, streets, orgs, titles):
        self.first_names = first_names
        self.last_names = last_names
        self.streets = streets
        self.orgs = orgs
        self.titles = titles

    def prepare(self):
        for lst in [self.first_names, self.last_names,
                    self.streets, self.orgs, self.titles]:
            random.shuffle(lst)

    def fill_card(self, target_fields, position):
        """Takes data and fills in fields, then creates a list of formatted
        lines that can be written into a .vcf file. Takes a position argument
        that it basically interprets as modulo the length of the list."""
        new_card = ["BEGIN:VCARD", "VERSION:2.1",]
        # Fill the Name field.
        if "Name" in target_fields:
            namefield = "N:"
            namefield += str(self.last_names[position % len(self.last_names)])
            namefield +=";"
            namefield += str(self.first_names[position % len(self.first_names)])
            new_card.append(namefield)
        if "FullName" in target_fields:
            fnamefield = "FN:"
            fnamefield += str(self.first_names[position % len(self.first_names)])
            fnamefield += " "
            fnamefield += str(self.last_names[position % len(self.last_names)])
            new_card.append(fnamefield)
        if "Organization" in target_fields:
            orgfield = "ORG:"
            orgfield += str(self.orgs[position % len(self.orgs)])
            new_card.append(orgfield)
        if "Title" in target_fields:
            titlefield = "TITLE:"
            titlefield += str(self.titles[position % len(self.titles)])
            new_card.append(titlefield)
        if "Phone" in target_fields:
            phonefield = "TEL;WORK;VOICE:("
            phonefield += str(random.randrange(100,999))
            phonefield += ") 555-"
            phonefield += "%04d" % random.randrange(0,9999)
            new_card.append(phonefield)
        if "Address" in target_fields:
            addrfield = "ADR;WORK:;;"
            addrfield += str(random.randrange(1,18234))
            addrfield += " "
            addrfield += str(self.streets[position % len(self.streets)])
            addrfield += ";Anytown;CA;12345;United States of America"
            new_card.append(addrfield)
        if "Email" in target_fields:
            emailfield = "EMAIL;PREF;INTERNET:"
            emailfield += str.lower(self.first_names[position % len(self.first_names)])
            emailfield += str.lower(self.last_names[position % len(self.last_names)])
            emailfield += "@example.com"
            new_card.append(emailfield)
        new_card.append("REV:%d" % random.randrange(100,500))
        new_card.append("END:VCARD")
        return new_card


def rolodex_engine(card_limit, target_fields):
    """Iterates over a range to generate a list of strings that can be
    sent to file or to stdout and which constitute a valid vcard file.
    Most programs that read vcards can accept a file that contains
    multiple vcards - all you have to do is concatenate them."""
    card_engine = CardFiller(first_names, last_names, streets, orgs, titles)
    card_engine.prepare()
    rolodex = []
    for i in range(1, card_limit+1):
        new_card = card_engine.fill_card(target_fields, i)
        for line in new_card:
            rolodex.append(line)
    return rolodex

################################### Execution ##################################

if __name__ == '__main__':
    """Run a variety of sanity checks regarding the arguments to the
    script.  If there are no command-line arguments, give the user a
    hint. If the arguments are weird, quit and ask them to try
    again. User input and the filesystem: two pain-in-the-butt parts
    of software engineering."""

    # Sanity checks.
    if len(sys.argv) != 3:
        print "This script requires exactly two arguments and python2: \n",
        print "* The number of vCards to generate \n",
        print  "* The name of the file to store them in. \n"
        sys.exit()
    if type(sys.argv[2]) != type("string"):
        print "The first argument must be a number, the second a name."
        sys.exit()
    try:
        int(sys.argv[1])
    except ValueError:
        print "The first argument must be a number, the second a name."
        sys.exit()
    if int(sys.argv[1]) > 2**16:
        print "Try generating less than 65,000 cards."
        sys.exit()
    if len(sys.argv[2]) > 128:
        print "Try a shorter filename."
        sys.exit()
    card_limit = int(sys.argv[1])
    card_export_file = sys.argv[2]
    # Writing to disk.
    try:
        with open("./%s" % card_export_file, "r") as rolodex_file:
            print "A file with that name already exists."
            sys.exit()
    except IOError, ioerr_msg:
        try:
            with open("./%s" % card_export_file, "w") as rolodex_file:
                rolodex = rolodex_engine(card_limit, target_fields)
                for c in rolodex:
                    rolodex_file.write(c)
                    rolodex_file.write("\n")
        except IOError, ioerr_msg:
            print "The script couldn't create a file for the vcards."
            print "The specific problem was '%s'" % ioerr_msg
