<?php

class DeviceController extends BaseController
{
	
	public function registerDevice()
	{
		$header = Input::all();
		$message = json_decode($header['message'], true);
		$processCode = (int) $message['process-code'];

		if($processCode == 40) {
			$device_id = (int) $message['device-id'];
			$device_type = $message['device-type'];
			$path = $header['path'];
			$registration_node_id = (int) $message['registration-node-id'];

			switch ($message['device-type']) {
				case 'EN':
					$this->registerNode($device_id, $device_type, $path, $registration_node_id);
					$response = CodeDescriptor::getResponseHeader(41);
					break;

				case 'IN':
					$this->registerNode($device_id, $device_type, $path, $registration_node_id);
					$response = CodeDescriptor::getResponseHeader(41);
					break;

				case 'WB':
					$this->registerWristband($device_id, $path, $registration_node_id);
					$response = CodeDescriptor::getResponseHeader(41);
					break;
				
				default:
					$response = CodeDescriptor::getResponseHeader(43);
					break;
			}
		}
		else
			$response = CodeDescriptor::getResponseHeader(42);

		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	}

	public function registerNode($id, $type, $path, $registrationNodeID)
	{
		$node = Node::find($id);
		if($node == NULL) {
			$node = new Node();
			$node->id = $id;
			$node->node_type = $type;
			$node->online_status = true;
			$node->save();
		}
		$node->register($path, $registrationNodeID);
	}

	public function registerWristband($id, $path, $registrationNodeID)
	{
		$wristband = Wristband::find($id);
		if($wristband == NULL) {
			$wristband = new Wristband();
			$wristband->id = $id;
			$wristband->online_status = true;
			$wristband->save();
		}
		$wristband->register($path, $registrationNodeID);
	}

	public function updateDeviceStatus()
	{
		$header = Input::all();
		$message = json_decode($header['message'], true);
		$processCode = (int) $message['process-code'];

		if($processCode == 80) {
			$device_id = (int) $message['device-id'];
			$device_type = $message['device-type'];

			switch ($message['device-type']) {
				case 'EN':
					Node::find($device_id)->updateStatus();
					$response = CodeDescriptor::getResponseHeader(11);
					break;

				case 'IN':
					Node::find($device_id)->updateStatus();
					$response = CodeDescriptor::getResponseHeader(11);
					break;

				case 'WB':
					Wristband::find($device_id)->updateStatus();
					$response = CodeDescriptor::getResponseHeader(11);
					break;
				
				default:
					$response = CodeDescriptor::getResponseHeader(12);
					break;
			}
		}
		else
			$response = CodeDescriptor::getResponseHeader(12);

		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	}

	public function genEvent()
	{
		$header = Input::all();
		$message = json_decode($header['message'], true);
		$processCode = (int) $message['process-code'];

		if($processCode == 90) {
			$device_id = (int) $message['device-id'];
			$device_type = $message['device-type'];
			$event_type = $message['event-type'];
			$event_detail = $message['event-detail'];

			switch ($message['device-type']) {
				case 'EN':
					Node::find($device_id)->genEvent($event_detail);
					$response = CodeDescriptor::getResponseHeader(11);
					break;

				case 'IN':
					Node::find($device_id)->genEvent($event_detail);
					$response = CodeDescriptor::getResponseHeader(11);
					break;

				case 'WB':
					Wristband::find($device_id)->genEvent($event_type, $event_detail);
					$response = CodeDescriptor::getResponseHeader(11);
					break;
				
				default:
					$response = CodeDescriptor::getResponseHeader(12);
					break;
			}
		}
		else
			$response = CodeDescriptor::getResponseHeader(12);

		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	}
}