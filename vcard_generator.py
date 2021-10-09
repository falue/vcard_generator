#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Generates an abitrary number of valid .vcf vCard contacts based on the
parameters set at the beginning of the file. See also:
http://softwareas.com/vcard-for-developers
http://en.wikipedia.org/wiki/VCard

Based on gist by brighid
https://gist.github.com/brighid/58519d5849701a1f4ec2
"""

import random, sys, os
import base64
import datetime

################################## Parameters ##################################

# We'll use this data no matter what the user tells us.

# What fields shall be populated?
target_fields = {"Name":True,
                 "FullName":True,
                 "Organization":True,
                 "Address":True,
                 "Title":True,
                 "Photo":True,
                 "Phone":True,
                 "Email":True,}

# Percentages of fields actually being populated (more randomness)
frequencyoforg = 33
frequencyoftitle = 10
frequencyofaddress = 75
frequencyofphoto = 40
frequencyofnoble = 3

# Data that we'll use to populate the cards' fields. Traditional swiss names.
first_names = ["Abi", "Adalie", "Aita", "Albula", "Alyssia", "Amrei", "Andel", "Andrin", "Andrin", "Anica", "Annatina", "Anneli", "Anneli", "Annely", "Annigna", "Annina", "Antonette", "Arale", "Arianita", "Armida", "Armide", "Atreju", "Ayla", "Badin", "Balz", "Barbli", "Beat", "Beat", "Beath", "Beath", "Bendicht", "Bendicht", "Benedikt", "Bengiamin", "Benjas", "Bensehilla", "Bern", "Bernhardin", "Berti", "Bethli", "Bigna", "Binia", "Brandi", "Carissima", "Chasper", "Chatrina", "Chatrina", "Chonz", "Cilgia", "Cla", "Conz", "Corina", "Corinne", "Corsica", "Dani", "Daron", "David", "Divico", "Dorli", "Dumeng", "Dumeni", "Dumeni", "Duri", "Eliane", "Elijan", "Elsa", "Elsi", "Elsy", "Elvezia", "Elvezia", "Emerita", "Emma", "Enie", "Erika", "Erina", "Ernestin", "Fabian", "Fabiola", "Fadri", "Ferdi", "Florin", "Florina", "Flurin", "Flurina", "Franklin", "Franzi", "Fränzi", "Fridolin", "Fridolina", "Friedolin", "Frillix", "Gaudenz", "Gian", "Gianin", "Gianrico", "Gieri", "Gilgian", "Gilgian", "Gillis", "Giuanna", "Giulitta", "Giusep", "Göpf", "Gritli", "Gritli", "Gwer", "Hänggi", "Hanneli", "Hanni", "Hans", "Hans-Rudolf", "Harri", "Heidi", "Heiri", "Helvetia", "Ingenuin", "Inglina", "Innegrit", "Irmalin", "Irmeli", "Irmelin", "Isalie", "Jelsha", "Jilge", "Jo", "Jockel", "Jocki", "Jocky", "Joder", "Jonin", "Jöri", "Jost", "Jovin", "Jovin", "Jürg", "Kaja", "Karin", "Katrin", "Ladina", "Lanessa", "Leon", "Levio", "Lisa", "Lisa-Maria", "Lisa-Katharina", "Lisi", "Loan", "Lorian", "Lorin", "Luc", "Ludewiga", "Lumi", "Lyan", "Madlaina", "Madleina", "Magali", "Marei", "Marilen", "Mark", "Markus", "Marleen", "Maya", "Meinrad", "Melia", "Melinda", "Menga", "Meret", "Midja", "Mylene", "Nando", "Neamy", "Nette", "Niklaus", "Nordin", "Norina", "Pascale", "Paschalis", "Ramona", "Reto", "Reto", "Rita", "Roger", "Rolf", "Rösli", "Ruedi", "Ruedi", "Sana", "Seina", "Selma", "Seraina", "Sereina", "Severin", "Severine", "Simon", "Susi", "Tell", "Töbe", "Ueli", "Urban", "Urs", "Ursina", "Uto", "Vera", "Vreni", "Vroni", "Walo", "Wendelin", "Rösi"]
last_names = ["Müller", "Meier", "Schmid", "Keller", "Weber", "Schneider", "Huber", "Meyer", "Steiner", "Fischer", "Baumann", "Frei", "Brunner", "Gerber", "Widmer", "Zimmermann", "Moser", "Graf", "Wyss", "Roth", "Suter", "Baumgartner", "Bachmann", "Studer", "Bucher", "Berger", "Kaufmann", "Kunz", "Hofer", "Bühler", "Lüthi", "Lehmann", "Marti", "Frey", "Christen", "Koch", "Egli", "Favre", "Arnold", "Pfister", "Schweizer", "Wüthrich", "Fuchs", "Martin", "Stalder", "Gasser", "Peter", "Kohler", "Maurer", "Koller", "Wenger", "Zürcher", "Burri", "Furrer", "Egger", "Hofmann", "Michel", "Hunziker", "Leuenberger", "Bieri", "Ammann", "Vogel", "Hug", "Hess", "Tanner", "Sutter", "Hauser", "Blaser", "Rüegg", "Hartmann", "Schuler", "Rey", "Wagner", "Gisler", "Senn", "Zbinden", "Kälin", "Schär", "Siegenthaler", "Scherrer", "Flückiger", "Lang", "Zaugg", "Fankhauser", "Stucki", "Kuhn", "Imhof", "Vogt", "Bernasconi", "Scheidegger", "Odermatt", "Portmann", "Küng", "Sommer", "Seiler", "Ackermann", "Liechti", "Jost", "Schmidt", "Schumacher", "Schärer", "Schwarz", "Stocker", "Staub", "Giger", "Hasler", "Schenk", "Rochat", "Lüscher", "Weiss", "Gloor", "Herzog", "Hofstetter", "Schwab", "Zehnder", "Stutz", "Pittet", "Rohner", "Weibel", "Schnyder", "Bosshard", "Wittwer", "Eichenberger", "Steiger", "Haas", "Schaller", "Stadelmann", "Rohrer", "Stettler", "Bolliger", "Stöckli", "Tobler", "Sieber", "Siegrist", "Wolf", "Sigrist", "Meister", "Marty", "Ulrich", "Lutz", "Lanz", "Blanc", "Röthlisberger", "Grob", "Kaiser", "Steffen", "Betschart", "Locher", "Beck", "Aeschlimann", "Blum", "Bühlmann", "Probst", "Mathys", "Rossi", "Schmutz", "Kessler", "Kuster", "Häfliger", "Muller", "Steinmann", "Stauffer", "Haller", "Graber", "Krebs", "Walker", "Ziegler", "Nussbaumer", "Benz", "Jenni", "Friedli", "Käser", "Bischof", "Fässler", "Hostettler", "Aebi", "Richard", "Hürlimann", "Zwahlen", "Knecht", "Schaub", "Wehrli", "Eugster", "Mäder", "Walther", "Ott", "Flury", "Brügger", "Rossier", "Willi", "Erni", "Ryser", "Gut", "Wicki", "Reber", "Merz", "Thalmann", "Mettler", "Wirth", "Iten", "Garcia", "Heiniger", "Glauser", "Schütz", "Niederberger", "Bürgi", "Mathis", "Schüpbach", "Forster", "Wirz", "Bigler", "Clerc", "Achermann", "Gross", "Frischknecht", "Zingg", "Etter", "Jäggi", "Bösch", "Braun", "Ferrari", "Balmer", "Walter", "Trachsel", "Allemann", "Schlegel", "Kern", "Jakob", "Walser", "Fehr", "Bianchi", "Schoch", "Von", "Geiser", "Bürki", "Gfeller", "Iseli", "Sidler", "Zeller", "Bader", "Ritter", "Reymond", "Leu", "Amstutz", "Landolt", "Da", "Stadler", "Felder", "Hänni", "Tschanz", "Ernst", "Eberle", "Bärtschi", "Näf", "Germann", "Schönenberger", "Wild", "Birrer", "Monney", "Emmenegger", "Hodel", "Minder", "Affolter", "Eggenberger", "Zemp", "Winkler", "Isler", "Wälti", "Messerli", "Wiederkehr", "Burkhalter", "Sonderegger", "Neuenschwander", "Brand", "Brun", "Herrmann", "Baur", "Hirschi", "Dubois", "Schlatter", "Perrin", "Krähenbühl", "Maillard", "Grossenbacher", "Jenny", "Zuber", "Schneeberger", "Aebischer", "Mosimann", "Linder", "Beyeler", "Fontana", "Perret", "Rieder", "Gehrig", "Stähli", "Hutter", "Buser", "Miller", "Thoma"]

# Some common swiss street names.
# Street numbers will be generated at random.
streets = ["Adligenswilerstrasse", "Badergässli", "Bahnhofstrasse", "Brandgässli", "Bruchstrasse", "Carl-Spitteler-Quai", "Denkmalstrasse", "Dorenbach", "Franziskanerplatz", "Gibraltarstsrasse", "Grabenstrasse", "Grendel", "Haldenstrasse", "Hans-Holbeingasse", "Hertensteinstrasse", "Hirschenplatz", "Jesuitenplatz", "Kapellplatz", "Kornmarkt", "Kramgasse", "Langensandstrasse", "Löwengraben", "Löwenstrasse", "Mühlenplatz", "Münzgasse", "Museggstrasse", "Nationalquai", "Obergrundstrasse", "Paradiesgässli", "Pfistergasse", "Pilatusstrasse", "Rathausquai", "Reusssteg", "Rosengart Platz", "Rössligasse", "Rütligasse", "Schlossergasse", "Schwanenplatz", "Schweizerhofquai", "St. Leodegarstrasse", "Sternenplatz", "Süesswinkel", "Unter der Egg", "Unterlöchli", "Voltastrasse", "Weggisgasse", "Weinmarkt", "Wesemlinstrasse", "Zentralstrasse", "Zürichstrasse"]

# Biggest swiss cities
city = ["Zürich", "Geneva", "Basel", "Lausanne", "Bern", "Winterthur", "Lucerne", "St. Gallen", "Lugano", "Biel/Bienne", "Thun", "Bellinzona", "Köniz", "Fribourg", "La Chaux-de-Fonds", "Schaffhausen", "Chur", "Vernier", "Uster", "Sion"]
# canton = ["ZH", "BE", "LU", "UR", "SZ", "OW", "NW", "GL", "ZG", "FR", "SO", "BS", "BL", "SH", "AR", "AI", "SG", "GR", "AG", "TG", "TI", "VD", "VS", "NE", "GE", "JU"]
canton = ["ZH", "GE", "BS", "VD", "BE", "ZH", "LU", "SG", "TI", "BE", "BE", "TI", "BE", "FR", "NE", "SH", "GR", "GE", "ZH", "VS"]
plz = ["8000", "1200", "4000", "1000", "3000", "8400", "6000", "9000", "6900", "2500", "3600", "6500", "3007", "1700", "2300", "8200", "7000", "1209", "8606", "1950"]

domains = ["gmx.ch", "gmx.net", "bluewin.ch", "hotmail.com", "gmail.com", "protonmail.com", "domainhost.com", "hostpoint.ch", "green.ch"]
orgs = ["Rest. Schild", "Restaurant Mimose", "Elektrotech GmbH", "Service Rapide GmbH", "Infotainment AG", "InnoService GmbH", "Fotoshoot2theMAXX GmbH", "Pleasure Nails AG", "Total Spa AG", "Hausreinigungen & So GmbH", "Schreiner Furrer AG", "Hauswartungen CreaLive AG", "Buchhaltung Burkhart GmbH", "FantasyLand Shopping AG", "Kinderparadies GmbH", "Bücherwurm AG", "Broki Zürich AG", "Autoservice", "Liefern & Lafern GmbH", "Audiocheck GmbH", "Maxx Soundstage AG"]
titles = ["Dr.", "Dr. Med.", "FH", "Dr", "MBA", "M.B.A.", "Dipl. Ing.", "Architekt FH", "Dipl. Zahnarzt", "Dr. Med. Dent."]

# Count all portrait photo images in faces/
path, dirs, files = next(os.walk("faces/"))
numberoffaces = len(files)-1

################################## Actions ###################################

class CardFiller:
    """A class whose instances take the basic dataset we're working with,
    shuffle it, and grind through generating VCard entries based on it. """
    def __init__(self, first_names, last_names, streets, orgs, titles):
        self.first_names = first_names
        self.last_names = last_names
        self.streets = streets
        self.city = city
        self.canton = canton
        self.plz = plz
        self.domains = domains
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
        new_card = ["BEGIN:VCARD", "VERSION:3.0",]

        # Upper class promotion
        if random.randint(0,100) < frequencyofnoble:
            noble = random.choice(["Von", "Van", "Zu"])
        else:
            noble = ''

        # Fill in the fields
        if "Name" in target_fields:
            namefield = "N:"
            namefield += str(self.last_names[position % len(self.last_names)])
            namefield +=";"
            namefield += str(self.first_names[position % len(self.first_names)])
            namefield +=";"
            if noble:
                namefield += noble
                namefield +=";"
            new_card.append(namefield)

        if "FullName" in target_fields:
            fnamefield = "FN:"
            fnamefield += str(self.first_names[position % len(self.first_names)])
            fnamefield += " "
            if noble:
                fnamefield += noble
                fnamefield += " "
            fnamefield += str(self.last_names[position % len(self.last_names)])
            new_card.append(fnamefield)

        if "Organization" in target_fields and random.randint(0,100) < frequencyoforg:
            orgfield = "ORG:"
            orgfield += str(self.orgs[position % len(self.orgs)])
            new_card.append(orgfield)

        if "Title" in target_fields and random.randint(0,100) < frequencyoftitle:
            titlefield = "TITLE:"
            titlefield += str(self.titles[position % len(self.titles)])
            new_card.append(titlefield)

        if "Photo" in target_fields and random.randint(0,100) < frequencyofphoto:
            filepath = "faces/"+str(random.randint(1,numberoffaces))+".jpg"
            with open(filepath, "rb") as imagefile:
                base64img = base64.b64encode(imagefile.read())
            photofield = "PHOTO;TYPE=JPEG;ENCODING=b:"
            photofield += base64img
            new_card.append(photofield)

        if "Phone" in target_fields:
            phonefield = "TEL;WORK;VOICE:"
            if random.randint(0,100) < 25:
                phonefield += "00 41 "
            elif random.randint(0,100) < 25:
                phonefield += "+41 "
            else:
                phonefield += "0"
            phonefield += "7"
            phonefield += "%01d" % random.randrange(6,9)
            phonefield += " "
            phonefield += "%03d" % random.randrange(100,999)
            phonefield += " "
            phonefield += "%02d" % random.randrange(10,99)
            phonefield += " "
            phonefield += "%02d" % random.randrange(10,99)
            new_card.append(phonefield)

        if "Address" in target_fields and random.randint(0,100) < frequencyofaddress:
            addrfield = "ADR;WORK:;;"
            addrfield += str(self.streets[position % len(self.streets)])
            addrfield += " "
            addrfield += str(random.randrange(1,250))
            if random.randint(0,100) < 15:
                addrfield += random.choice(["A", "B", "C", "a", "b", "c", ".1", ".2", "-A", "-B", "-C"])
            addrfield += ";"
            addrfield += str(self.city[position % len(self.city)])
            addrfield += ";"
            addrfield += str(self.canton[position % len(self.canton)])
            addrfield += ";"
            addrfield += str(self.plz[position % len(self.plz)])
            addrfield += ";Switzerland"
            new_card.append(addrfield)

        if "Email" in target_fields:
            emailfield = "EMAIL;PREF;INTERNET:"
            specialcharmap = {
                ord(u'Ä'): u'Ae',
                ord(u'Ü'): u'Ue',
                ord(u'Ö'): u'Oe',
                ord(u'ä'): u'ae',
                ord(u'ü'): u'ue',
                ord(u'ö'): u'oe',
                }
            firstname = unicode(str.lower(self.first_names[position % len(self.first_names)]), "utf-8").translate(specialcharmap)
            lastname = unicode(str.lower(self.last_names[position % len(self.last_names)]), "utf-8").translate(specialcharmap)
            if random.randint(0,100) < 50:
                emailfield += "{}{}".format(firstname, lastname)
            elif random.randint(0,100) < 50:
                emailfield +=  "{}.{}".format(firstname[0], lastname)
            elif random.randint(0,100) < 50:
                emailfield +=  "{}{}".format(firstname, str(random.randrange(75,99)))
            else:
                emailfield += lastname
            emailfield += "@"
            emailfield += str(self.domains[position % len(self.domains)])
            new_card.append(emailfield)

        # Create fake revision timestamp in the past up to two years ago
        now = datetime.datetime.now()
        randomedittime = now - datetime.timedelta(seconds=random.randrange(0,60*60*24*30*12*2))
        new_card.append("REV:%s" % randomedittime.strftime('%Y%m%dT%H%M%SZ'))  # revision date; format: 20140301T221110Z
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
        print "This script requires exactly two arguments (and python2!): \n",
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
        print "Try generating less than 65,000 cards you weirdo."
        sys.exit()
    if len(sys.argv[2]) > 128:
        print "Try a shorter filename."
        sys.exit()
    card_limit = int(sys.argv[1])
    card_export_file = "{}.vcard".format(sys.argv[2])

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
                print "Successfully created file '{}' with {} cards.".format(card_export_file, card_limit)
        except IOError, ioerr_msg:
            print "The script couldn't create a file for the vcards."
            print "The specific problem was '%s'" % ioerr_msg
