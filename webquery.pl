#!/usr1/bin/perl5
#
# This program gets the output of a specified URL.  The user
# specifies the host and URL as well as any parameters that might
# be used by the URL.  The output of URL is returned either
# to standard output or to a specified file.  Five special keyword
# parameters may be specified: url, host, method, port and file.
# All other parameters are passed to the URL.
#
# Webquery does no reformatting or error checking.  Typically
# the returned data will be an HTML formatted document.  If an
# error is encountered, the returned data may be an HTML formatted
# error message.
#
# Usage:
# webquery.pl url=URL host=HOST method=METHOD port=PORT file=FILE [key=VALUE key=VALUE]
#
# The default URL is the null string. The default host is the local
# host.  The method and port keywords may be used
# to override the defaults of POST and 80 respectively.
# The file keyword specifies an output file to which the response is
# to be sent.  If not specified, output is sent to standard output.
#
#
# Additional keywords are appended to the URL request as
# keyword values for a forms request.  Webquery will appropriately
# escape special characters.
#

use Socket;

$port = 80;
$method = "POST";

# Loop over the locally handled arguments.

foreach (@ARGV) {
    if (/=/) {
        ($key, $value) = split(/=/);
	
	if ($key eq "url") { $url = $value;}
	elsif ($key eq "host") {$host = $value;}
	elsif ($key eq "method") {$method = $value;}
	elsif ($key eq "port") {$port = int($value);}
	elsif ($key eq "file") {$outfile = $value;}
    }
}

if (!$url) {
    $url = "";
}

if (!$host) {
    chop ($host = `hostname`);
}

# Set up the socket connection.
#   Socket code below adapted from "Programming Perl", by Wall and Schwartz.
#

$sockaddr = 'S n a4 x8';

chop ($hostname = `hostname`);

($name, $aliases, $proto) = getprotobyname('tcp');

$thisaddr = Socket::inet_aton($hostname);
$thataddr = Socket::inet_aton($host);

$this = Socket::pack_sockaddr_in(0,$thisaddr);
$that = Socket::pack_sockaddr_in($port,$thataddr);

# Make the socket file handle
if (socket(S, AF_INET, SOCK_STREAM, $proto)) {
} else {
    die("Webquery: Unable to create socket");
}

if (bind(S, $this)) {
} else {
    die ("Webquery: Unable to bind socket, $!");
}

if (connect(S, $that)) {
} else {
    die("Webquery: Unable to connect to $host, $!");
}

# Make the socket the default output
select (S);

# Force immediate flushing of output
$| = 1;

# Go back to standard output.
select (STDOUT);

# Format the query string.  We'll loop over all the
# arguments again and this time we'll ignore the
# special ones.

args_loop:
foreach (@ARGV) {
    if (/=/) {
        ($key, $value) = split("=", $_, 2);
	if ($key eq "host"  ||
	    $key eq "url"   ||
	    $key eq "port"  ||
	    $key eq "method"||
	    $key eq "file") {
	        next args_loop;
        }
	
	# Put in field delimiter.
	if ($query) {$query .= "&";}
	
	# Escape special characters.  Note that
	# we do it for key and value separately so as not to
	# escape the '='.
	
	$query .= &webcode($key);
	$query .= "=";
	$query .= &webcode($value);
	
    } else {
    
        # Allow generic strings too.
        if ($query) {$query .= "&";}
	$query .= &webcode($value);
    }
}

# Put in characters to ensure query termination.  There seems to
# be an extra \015, but we seem to need this sometimes.
if ($query) {$query .= "\015\012\012";}


$method =~ tr/a-z/A-Z/;
# Send the query to the server.
if ($query){
    if ($method eq 'POST') {
        print S "$method $url HTTP/1.0\012",
          "User_Agent: Webquery.pl V1.0\012",
          "Content-type: application/x-www-form-urlencoded\012",
          "Content-length: ",length($query)-3,"\012\012";
        print S $query;
    } else {
        print S "$method $url"."?".$query."HTTP/1.0\012",
          "User_Agent: Webquery.pl V1.0\012",
          "Content-type: application/x-www-form-urlencoded\012";
    }
} else {
    # Usually we can only use POST if there are parameters, so convert
    # to GET if not.
    if ($method eq "POST") {$method = "GET";}
    print S "$method $url HTTP/1.0\012",
      "User_Agent: Webquery.pl V1.0\012\012";
}

# If the user specified an output file, open it and make it
# the standard output.
if ($outfile) {
    open(OUTFILE, '>'.$outfile);
    select(OUTFILE);
}
    
# Now read the results.
while ( ($len = read(S, $buffer, 1024)) > 0) {
    print $buffer;
}

sub webcode {

local ($string) = @_;

# First convert special characters to to %xx notation.
$string =~ s/[^ a-zA-Z0-9]/sprintf("%%%02x", ord($&))/eg ;

# Now convert the spaces to +'s.
# We do this last since otherwise +'s would be translated by above.
$string =~ tr/ /+/;

# Perl doesn't require (or even like) putting in the return value,
# but I find it clearer.
return $string;
}
