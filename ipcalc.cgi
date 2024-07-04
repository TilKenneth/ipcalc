#!/usr/bin/perl  

# CGI Wrapper for IPv4 Calculator
# 
# Copyright (C) Krischan Jodies 2000 - 2021
# krischan()jodies.de, https://jodies.de/ipcalc
# 
# Copyright (C) for the graphics ipcalc.gif and ipcalculator.png 
# Frank Quotschalla. 2002 
#  
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


# 0.14.3
# 0.15      25.09.2000   Added link to this wrapper
# 0.16      07.11.2000   Get version from ipcalc
# 0.17      09.01.2001   Added screenshot
# 0.18      02.02.2001   Played with the html
# 0.18.1    03.02.2001   Played even more with the html
# 0.19      01.04.2001   Help text for wildcard netmask / Credits
# 0.20      20.05.2001   Changed error messages
# 0.21      19.06.2001   Adapted to new -c option
# 0.22      30.07.2002   Stole javascript at dict.leo.org
# 0.23      28.10.2004   Remove whitespace in input fields
#                        Idea by David Shirlay David.Shirley(a)team.telstra.com
# 0.24      07.07.2005   Added license text to cgi-wrapper. Add style into cgi script
# 0.25      11.01.2006   Link to screenshot was wrong.
# 0.26      27.07.2006   Replaced REQUEST_URI with SCRIPT_URL to prevent cross-site-scripting attacks
# 0.26.1-ki 05.07.2024   get_ipcalc() to test path or current dir for 'ipcalc'

$|=1;

use File::Spec::Functions 'catfile';

sub get_ipcalc() {
   $filename = "$ENV{SCRIPT_FILENAME}";
   $filename=~m/^.+\//;
   $path=$&;
   $retval = catfile($path, 'ipcalc');
	$default = "/usr/local/bin/ipcalc";
	($retval = $default) if -x $default; 
	return $retval;
}

$ipcalc = get_ipcalc();
$MAIL_ADDRESS="ipcalc-200502&#64;jodies.de";
# history:
# 200404 
$actionurl = $ENV{'SCRIPT_URL'};
$actionurl =~ s/&/&amp;/g;
use CGI;
$query = new CGI;
$host  = $query->param('host');
$mask1 = $query->param('mask1');
$mask2 = $query->param('mask2');
$help  = $query->param('help');

$host  =~ s/ //g;
$mask1 =~ s/ //g;
$mask2 =~ s/ //g;


$version = qx($ipcalc -v);
chomp $version;

if (! defined $host) {
	$host = '';
}

if (! defined $mask1) {
	$mask1 = '';
	$help = 1;
}

if (! defined $mask2) {
	$mask2 = '';
}

if ($mask2 eq $mask1) {
	$mask2 = '';
}

if ($host eq '') {
	$host = '192.168.0.1';
}

$testhost = $host;
$testhost =~ s/\.//g;
if ($testhost !~ /^\d+$/) {
	$host = '192.168.0.1';
}


if ($mask1 eq '') {

}


$testhost = $mask1;
$testhost =~ s/\.//g;
if ($testhost !~ /^\d+$/) {
	$mask1 = 24;
}

if ($mask2 ne '') {
	$testhost = $mask2;
	$testhost =~ s/\.//g;
	if ($testhost !~ /^\d+$/) {
		$mask2 = '';
	}
}


print $query->header(-type => "text/html", -charset => "UTF-8");
print << "EOF";
<!DOCTYPE html>
<html lang="en">
   <head> 
      <meta charset="utf-8">
      <meta translate="no">
      <meta name="robots" content="noindex, nofollow">
      <title>IP Calculator / IP Subnetting - (TilKenneth/internal)</title>

      <meta name="generator" content="ipcalc $version (TilKenneth/internal)">
      <meta name="keywords" content="ipcalc-internal,ipv4,ipv6,subnet,netmask,calculator">
      <meta name="author" content="Krischan Jodies, Github/TilKenneth">
      <meta name="application-name" content="ipcalc $version (TilKenneth/internal)">
      <meta name="description" content="ipcalc (TilKenneth/internal) report by https://github.com/TilKenneth/ipcalc/tree/internal">
      
   
   <script language="JavaScript" type="text/javascript">
      <!-- 
      function setFocus()
      {
         document.form.host.focus();
         document.form.host.select();
      }
      // -->
   </script>

<style>
<!--
body {
   background-color: white;
   color: black;
   font-family: "Trebuchet MS", Verdana, Geneva, Helvetica, sans-serif;
}

A {text-decoration:none; color:#003CD7; }
A:visited {color:#003CD7;}
A:hover {background-color:#dddddd;}

h1 {
   margin-bottom: 30px;
}

table {
	border-spacing: 1px;
	border-style: solid;
	border-color: #888888;
	border-width: 0px;
}


input.text {
   border: solid 1px #000000;
}

.help {
   cursor:help;
}

input:focus, textarea:focus {
   background-color: #e9edf5;
}

div#help {
   border-color: black;
   border-style: dotted;
   border-width: 0px;
   border-spacing: 5px;
   margin: 5px;
   margin-bottom: 10px;
}

div#formfield {
   border-color: black;
   border-style: dotted;
   border-width: 1px;
   border-spacing: 5px;
   margin: 5px;
   padding: 5px;
}

-->
</style>
</head>
<body onLoad="setFocus()">
EOF
#print "$ENV{HTTP_USER_AGENT}<br>\n";

print << "EOF";
<center>


<table cellpadding=15 border=0 cellspacing=50><tr><td bgcolor="#ffffff">
<table border=0 width="100%">
<tr>
<td valign="top">&nbsp;</td>
<td>&nbsp;</td></tr>
</table>
EOF
if ($help) {
print << "EOF";

EOF
}

print <<"EOF";
<div id="formfield">
   <form action="$actionurl" method="get" name="form" id="form">
   <table border=0>
   <tr>
      <td><b>Address</b> (Host or Network)</td>
      <td><b>Netmask</b> (i.e. 24)</td>
      <td><b>Netmask</b> for sub/supernet (optional)</td>
   </tr>
   <tr>
   <td nowrap><input class=text name=host value="$host"> / </td>
   <td nowrap><input class=text name=mask1 value="$mask1"></td>
   <td nowrap> move to: <input class=text name=mask2 value="$mask2"></td>
   </tr>
   <tr>
      <td colspan=3>
      <input class=submit type="submit" value="Calculate">
EOF
if (! $help) {
   print '&nbsp;<input name=help class=help type="submit" value="Help">';
}
print <<"EOF"; 
      </td>
   </tr>
   </table>
   </form>
</div>

<p>

EOF

if (defined $error) {
	$error =~ s/</&lt;/gm;
	$error =~ s/>/&gt;/gm;
	$error =~ s/\n/<br>/g;
	print qq(<font color="#ff0000"><tt>\n);
	print "$error<br>";
	print qq(</tt><font color="#000000">\n);
	
}

system("$ipcalc -h $host $mask1 $mask2");

print <<"EOF";

<hr>
This is a modified version of the original, the modifications are hosted at <a href="https://github.com/TilKenneth/ipcalc/tree/internal">https://github.com/TilKenneth/ipcalc/tree/internal</a>.
<br>
</center>
</body>
</html>
EOF
