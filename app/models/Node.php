<?php

class Node extends Eloquent {

	public function registration() { return $this->hasMany('NodeRegistration','node_id'); }
	public function node_registration() { return $this->hasMany('NodeRegistration','registration_node_id'); }
	public function event() { return $this->hasMany('NodeEvent','node_id'); }
	public function wristband_registration() { return $this->hasMany('WristbandRegistration','registration_node_id'); }

	public function register($path, $registrationNodeID)
	{
		$registration = new NodeRegistration;
		$registration->node()->associate($this);
		$registration->path = $path;
		$registration->registration_node()->associate(Node::find($registrationNodeID));
		$registration->save();
	}

	public function updateStatus()
	{
		$this->online_status = false;
		$this->save();
		$this->online_status = true;
		$this->save();
	}

	public function	genEvent($detail)
	{
		$event = new NodeEvent;
		$event->node()->associate($this);
		$event->detail = $detail;
		$event->save();
	}
}