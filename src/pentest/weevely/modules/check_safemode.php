//Description: Check PHP safe mode options.
$s='safe_mode'; $o='open_basedir'; $d='disable_functions'; $g='safe_mode_gid';
//@ini_restore($s); @ini_set($s,0);
//@ini_restore($o); @ini_set($o,'');
//@ini_restore($d); @ini_set($d,'');
//@ini_restore($g); @ini_set($g,'');
print($s . " = " . @ini_get('safe_mode') . "\n");
print($d . " = " . @ini_get('disable_functions') . "\n");
print($o . " = " . @ini_get('open_basedir') . "\n");
print($g . " = " . @ini_get('safe_mode_gid') . "\n");