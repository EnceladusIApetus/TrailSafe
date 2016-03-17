<?php

class NodeEvent extends Eloquent
{
	
	protected $table = 'node_events';

	public function node()   { return $this->belongsTo('Node','node_id');}
}