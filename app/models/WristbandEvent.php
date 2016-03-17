<?php

class WristbandEvent extends Eloquent
{
	
	public function wristband()   { return $this->belongsTo('Wristband','wristband_id');}
	public function user()   { return $this->belongsTo('User','user_id');}
}