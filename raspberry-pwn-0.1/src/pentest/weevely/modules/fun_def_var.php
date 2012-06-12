//Author: Carlo Satta
//Description: Print all functions (f), variables (v), constants (c).
//Arguments: type
foreach(str_split($ar[0]) as $l){
	if($l=='f')print_r(get_defined_vars());
	elseif($l=='v')print_r(get_defined_constants());
	elseif($l=='c')print_r(get_defined_functions());
	else echo 'WUT?';
}
