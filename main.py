# -*- coding: utf-8 -*-

from Http import Http
from Settings import IDUL, PASW
import re

menu = '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" /> \
        <link rel="stylesheet" media="screen" type="text/css" href="style.css" /> \
        Copyright <a href="http://agilbert.name/">Alain Gilbert</a> (<a href="http://twitter.com/#!/alain_gilbert">@alain_gilbert</a>) \
        <ul> \
        <li><a href="horaire.html">Horaire</a></li> \
        <li><a href="compte.html">Frais de scolarite</a></li> \
        <li><a href="dossier.html">Dossier scolaire</a></li> \
        </ul>'
http = Http()
http.get('https://capsuleweb.ulaval.ca/pls/etprod7/twbkwbis.P_WWWLogin')
http.post('https://capsuleweb.ulaval.ca/pls/etprod7/twbkwbis.P_ValLogin', { 'sid': IDUL, 'PIN': PASW })

with open('main.html', 'w+') as f:
   f.write(menu)

res = http.get('https://capsuleweb.ulaval.ca/css/Y_web_defaultapp.css')
with open('style.css', 'w+') as f:
   f.write(res)

res = http.get('https://capsuleweb.ulaval.ca/pls/etprod7/bwskfshd.P_CrseSchd')
with open('horaire.html', 'w+') as f:
   c = re.compile('(<TABLE\s\sCLASS="datadisplaytable"(.*?)">.+?)<!--\s\s\*\* START', re.S)
   t = c.search(res).group(1)
   f.write(menu)
   f.write(t)

res = http.get('https://capsuleweb.ulaval.ca/pls/etprod7/bwskoacc.P_ViewAcctTotal')
with open('compte.html', 'w+') as f:
   c = re.compile('<TABLE  CLASS="datadisplaytable"(.*?)">(.+?)<!--\s\s\*\* START', re.S)
   t = c.search(res).group(2)
   f.write(menu)
   f.write(t)

res = http.post('https://capsuleweb.ulaval.ca/pls/etprod7/bwskgstu.P_StuInfo', { 'term_in': '201109' })
with open('dossier.html', 'w+') as f:
   c = re.compile('<DIV class="pagetitlediv">(.+?)<!--\s\s\*\* START', re.S)
   t = c.search(res).group(1)
   f.write(menu)
   f.write(t)
