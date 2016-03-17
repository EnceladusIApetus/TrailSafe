<?php

class NodeRegistration extends Eloquent
{
	protected $table = 'node_registration';

	public function node()   { return $this->belongsTo('Node','node_id');}
	public function registration_node()   { return $this->belongsTo('Node','registration_node_id');}
}