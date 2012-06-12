//Author: Carlo Satta
//Arguments: name, url
//Description: Download a file. Specify complete path ('writabledir/file.html') and complete url (http://url)
echo file_put_contents($ar[0], file_get_contents($ar[1]))."\n";
