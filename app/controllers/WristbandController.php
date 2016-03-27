<?php

class WristbandController extends BaseController
{

	public function findByID()
	{
		return Wristband::find(Input::get('device-id'));
	}

	public function getWristbandsAroundNode()
	{
		$node = Node::find(Input::get('device-id'));
		$wristband_registrations = $node->wristband_registration()->where('active', '=', true)->get();

		$wristbands = array();
		foreach ($wristband_registrations as $key => $registration) {
			array_push($wristbands, $registration->wristband()->get()[0]);
		}
        return $wristbands;
	}

	public function checkEmergencyResponse()
	{
		$head = Input::all();

		if(isset($head['message'])) {
			$message = json_decode($head['message'], true);
			$id = $message['device-id'];
		}
		else
			$id = $head['device-id'];

		$wristband = Wristband::find($id);
		if(isset($wristband)) {
			$event = $wristband->event()->where('type', '=', 1)->get()->pop();
			$response = CodeDescriptor::getResponseHeader(11);
			if($event->status == 1)
				$response['emergency-status'] = 93;
			else
				$response['emergency-status'] = 95;
		}
		else
			$response = CodeDescriptor::getResponseHeader(11);

		return json_encode($response);
	}

	public function	getDeviceInDanger()
	{
		$emerge_events = WristbandEvent::where('status', '=', 0)->get();
		$wristbands = array();
		foreach ($emerge_events as $key => $event) {
			array_push($wristbands, $event->wristband()->get());
		}

		return $wristbands;
	}

	public function	updateDeviceInSafe()
	{
		$wristband = Wristband::find(Input::get('device-id'));
		$emerge_events = $wristband->event()->get()->pop();

		if(isset($emerge_events) && $emerge_events->status == 1) {
			$wristband->updateEmergeSafeStatus();
			return 'true';
		}

		return 'false';
	}

	public function	responseEmergency()
	{
		$wristband = Wristband::find(Input::get('device-id'));
		$emerge_events = $wristband->event()->where('type', '=', 1)->get()->pop();

		if(isset($emerge_events) && $emerge_events->status == 0) {
			$wristband->responseEmergeStatus();
			return 'true';
		}

		return 'false';
	}

	public function checkRiskStatus()
	{
		$message = json_decode(Input::get('message'), true);
		$wristband = Wristband::find($message['device-id']);
		$node = $wristband->registration()->get()->pop()->registration_node()->get()[0];

		$response = CodeDescriptor::getResponseHeader(11);

		if($node->risk_status == 1)
			$response['risk-status'] = 111;
		else
			$response['risk-status'] = 112;

		return json_encode($response);
	}
}