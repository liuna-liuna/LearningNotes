
$file = "";
$file = $ARGV[0];

$user = "service.tip.cvom";
$group= "global";

if ($file eq "")
{
	print "Usage: $0 <file>\n";
	exit 0;
}

@file = ($file);
print "Chowning the file $file to $user:$group\n";
$number = chown $user, $group, "$file";
print "Number of ownerships changed: $number\n";

exit 0;


# ref doc:	http://superuser.com/questions/624449/chown-function-in-perl

