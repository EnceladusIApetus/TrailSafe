<?php

class WristbandRegistration extends Eloquent
{
	
	protected $table = 'wristband_registration';

	public function wristband()   { return $this->belongsTo('Wristband','wristband_id');}
	public function registration_node()   { return $this->belongsTo('Node','registration_node_id');}
}