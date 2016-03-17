<?php

class NodeController extends BaseController {

	public function updateGPSCoordinate()
	{
		$message = json_decode(Input::get('message'), true);
		$node = Node::find((int) $message['device-id']);
		$node->latitude = $message['latitude'];
		$node->longitude = $message['longitude'];
		$node->save();
		$response = CodeDescriptor::getResponseHeader(11);
		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	}

	public function getAllNodes()
	{
		return Node::all();
	}

	public function getAllNodesStatus()
	{
		$nodes = Node::all();
		$nodesStatus = array();
		foreach ($nodes as $key => $node) {
			$lastUpdatedTime = new DateTime($node->updated_at);
			$currentTime = new DateTime();
			$diff =  (int) $lastUpdatedTime->diff($currentTime)->i;
			if($diff > 10) {
				$node->online_status = false;
				$node->save();
			}
			$nodesStatus[$node->id] = $node->online_status;
		}

		return json_encode($nodesStatus);
	}

	public function getNodeStatus()
	{
		$node = Node::find(Input::get('device-id'));
		$lastUpdatedTime = new DateTime($node->updated_at);
		$currentTime = new DateTime();
		$diff =  (int) $lastUpdatedTime->diff($currentTime)->i;
		if($diff > 10)
			$node->online_status = false;
			$node->save();
		return $node->online_status;
	}

	public function refreshNode()
	{
		$nodes = Node::all();
		foreach ($nodes as $key => $node) {
			$lastUpdatedTime = new DateTime($node->updated_at);
			$currentTime = new DateTime();
			$diff =  (int) $lastUpdatedTime->diff($currentTime)->i;
			if($diff > 10) {
				$node->online_status = false;
				$node->save();
			}
		}
	}

	public function getOfflineNodes()
	{
		$this->refreshNode();
		$nodes = Node::where('online_status', '=', false)->get();
		return json_encode($nodes);
	}

	public function getOnlineNodes()
	{
		$this->refreshNode();
		$nodes = Node::where('online_status', '=', true)->get();
		return json_encode($nodes);
	}

	public function updateStatus()
	{
		$message = json_decode(Input::get('message'), true);
		$node = Node::find((int) $message['device-id']);
		$node->online_status = true;
		$node->save();
		$response = CodeDescriptor::getResponseHeader(11);
		$response['receiver'] = Input::get('sender');
		return json_encode($response);
	}

}