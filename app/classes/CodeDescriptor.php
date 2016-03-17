<?php

class CodeDescriptor {

    public static function getDescription($code)
    {
		$string = file_get_contents("/var/www/html/TrailSafe/app/others/code_description.ini");
		$json_a = json_decode($string, true);
		return $json_a[$code];
    }

    public static function getResponseHeader($code)
    {
    	$response = array();
		$response['process-code'] = $code;
		$response['process-description'] = CodeDescriptor::getDescription((string) $code);
		return $response;
    }
}