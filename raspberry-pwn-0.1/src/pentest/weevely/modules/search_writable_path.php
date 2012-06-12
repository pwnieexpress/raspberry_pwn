//Author: Carlo Satta
//Description: Print all writable directories.
//OS: Linux
@swp($_SERVER['DOCUMENT_ROOT']);
function swp($d){
	$h = @opendir($d);
	while ($f = @readdir($h)) {
		$df=$d.'/'.$f; 
		if((@is_dir($df))&&($f!='.')&&($f!='..')){
			if(@is_writable($df)) echo "Writable: ".@str_replace($_SERVER['DOCUMENT_ROOT'],'',$df)."\n";
			@swp($df);
		}
	}
	@closedir($h);
}
