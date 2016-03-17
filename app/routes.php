<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the Closure to execute when that URI is requested.
|
*/

Route::get('/', function()
{
	return View::make('hello');
});

Route::group(array('prefix' => 'test/'), function(){
	Route::get('/', function() {return 'online';});
	Route::post('serverconnection', function()
	{
		$response = array();
		$response['process-code'] = 10;
		$response['process-description'] = CodeDescriptor::getDescription('10');
		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	});
});

Route::group(array('prefix' => 'user/'), function(){
	Route::get('getusers', 'UserController@getUserAroundNode');
	Route::get('register', 'UserController@register');
	Route::get('unregister', 'UserController@unregister');
	Route::any('find_by_id', 'UserController@findByID');
});

Route::group(array('prefix' => 'device/'), function(){
	Route::post('register', 'DeviceController@registerDevice');
	Route::post('updatestatus', 'DeviceController@updateDeviceStatus');
	Route::post('event', 'DeviceController@genEvent');
});

Route::group(array('prefix' => 'node/'), function(){
	Route::get('getstatus', 'NodeController@getNodeStatus');
	Route::get('getofflinenodes', 'NodeController@getOfflineNodes');
	Route::get('getonlinenodes', 'NodeController@getOnlineNodes');
	Route::get('updategps', 'NodeController@updateGPSCoordinate');
	Route::get('allnodes', 'NodeController@getAllNodes');
	Route::get('getallnodesstatus', 'NodeController@getAllNodesStatus');
	Route::any('find_by_id', 'NodeController@findByID');
});

Route::group(array('prefix' => 'wristband/'), function(){
	Route::get('getwristbands', 'WristbandController@getWristbandsAroundNode');
	Route::any('check_response', 'WristbandController@checkEmergencyResponse');
	Route::any('in_danger', 'WristbandController@getDeviceInDanger');
	Route::any('update_safe_device', 'WristbandController@updateDeviceInSafe');
	Route::any('find_by_id', 'WristbandController@findByID');
});