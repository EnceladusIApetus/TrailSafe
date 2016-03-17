<?php

class Wristband extends Eloquent
{
	public function registration() { return $this->hasMany('WristbandRegistration','wristband_id'); }
	public function event() { return $this->hasMany('WristbandEvent','wristband_id'); }
	public function user() { return $this->hasMany('User','wristband_id'); }

	public function register($path, $registrationNodeID)
	{
		$oldRegistration = $this->registration()->get()->pop();
		if($oldRegistration != null) {
			$oldRegistration->active = false;
			$oldRegistration->save();
		}

		$registration = new WristbandRegistration;
		$registration->wristband()->associate($this);
		$registration->path = $path;
		$registration->registration_node()->associate(Node::find($registrationNodeID));
		$registration->active = true;
		$registration->save();
	}

	public function updateStatus()
	{
		$this->online_status = false;
		$this->save();
		$this->online_status = true;
		$this->save();
	}
}