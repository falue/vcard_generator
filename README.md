# vcard generator
If you need to fill your DB or device with real-looking dummy data (vcard contacts), you're in luck, this is for you. This generates 1-65000 contact names and addresses in a single vcard file to be imported in your contacts app.

This repo is relying heavily on the gist by brighid:
https://gist.github.com/brighid/58519d5849701a1f4ec2

I increased the diversity of various fields, added base64 encoded profile images, added UTF-8 support for those fancy äöü's, and also localized it to my region (switzerland).
Your use case may differ.

## Use it
```
python2 vcard_generator.py 100 filename
```
This creates a file with the name "filename.vcard" containing 100 random contacts. You may be able to create up to 65,000 cards at once.

## Adjust it
- `add_class_field` *Mark generated cards with the class "vcard_generator" for easy finding fake contacts. Highly recommended to leave it True.*
- `target_fields` *delete the fields in this list you'll never want to show up*
- `frequency_of_org` *Frequency of an associated company to show up (0=never, 100=always)*
- `frequency_of_title` *Frequency of a title to show up (0=never, 100=always)*
- `frequency_of_address` *Frequency of an address to show up (0=never, 100=always)*
- `frequency_of_photo` *Frequency of a user image to show up (0=never, 100=always). Be aware that some software might not like it if you import 50K cards with 50K images at once.*
- `frequency_of_noble` *Frequency of a noble title to show up (0=never, 100=always)*

## Localize it
Adjust the following lists to your liking to match your target area.
```
first_names
last_names
streets
city
canton
plz
domains
orgs
titles
```

## See it
```
BEGIN:VCARD
VERSION:3.0
N:Zürcher;Lorian;
FN:Lorian Zürcher
TEL;WORK;VOICE:0041 78 600 10 51
ADR;WORK:;;Pilatusstrasse 248;La Chaux-de-Fonds;NE;2300;Switzerland
EMAIL;PREF;INTERNET:lorian80@protonmail.com
CLASS:vcard_generator
REV:20200803T143131Z
END:VCARD
```
```
BEGIN:VCARD
VERSION:3.0
N:Röthlisberger;Joder;
FN:Joder Röthlisberger
PHOTO;TYPE=JPEG;ENCODING=b:/9j/base64string...
TEL;WORK;VOICE:077 344 95 75
ADR;WORK:;;Schwanenplatz 24b;Biel/Bienne;BE;2500;Switzerland
EMAIL;PREF;INTERNET:joderroethlisberger@bluewin.ch
CLASS:vcard_generator
REV:20200610T112722Z
END:VCARD
```
*More examples in the example folder.*
