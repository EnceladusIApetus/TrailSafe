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

	public function	genEvent($event_type, $detail)
	{
		$oldEvent = $this->event()->where('type', '=', $event_type)->get()->pop();
		if($oldEvent != null && $oldEvent->status == 0) {
			$oldEvent->status = 2;
			$oldEvent->save();
		}

		$event = new WristbandEvent;
		$event->wristband()->associate($this);
		$event->user()->associate($this->user()->get()->pop());
		$event->type = $event_type;
		$event->detail = $detail;
		$event->save();
		return $event;
	}

	public function	updateEmergeSafeStatus()
	{
		$event = $this->genEvent(1, 'The user is safe now.');
		$event->status = 3;
		$event->save();
	}

	public function	responseEmergeStatus()
	{
		$event = $this->genEvent(1, 'The emergency request has been response.');
		$event->status = 1;
		$event->save();
	}
}