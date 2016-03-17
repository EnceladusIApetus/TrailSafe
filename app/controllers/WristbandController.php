<?php

class WristbandController extends BaseController
{

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
}