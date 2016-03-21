<?php

class UserController extends BaseController
{

	public function findByID()
	{
		return User::find(Input::get('user-id'));
	}

	public function getAllUser()
	{
		return User::all();
	}

	public function register()
	{
		$input = Input::all();
		$wristband = Wristband::find($input['wristband-id']);
		$user = new User();
		$user->wristband()->associate($wristband);
		$user->identifier = $input['identifier'];
		$user->name = $input['name'];
		$user->status = 1;
		$user->profile_pic = $input['profile-picture'];
		$user->save();
		$wristband->enable = true;
		$wristband->save();
	}

	public function unregister()
	{
		$input = Input::all();
		$user = User::find($input['user-id']);
		$user->status = 0;
		$user->save();
		$wristband = $user->wristband()->get();
		$wristband->enable = true;
		$wristband->save();
	}

	public function getUserAroundNode()
	{
		$node = Node::find(Input::get('device-id'));
		$wristband_registrations = $node->wristband_registration()->where('active', '=', true)->get();

		$user = array();
		foreach ($wristband_registrations as $key => $registration) {
			array_push($user, $registration->wristband()->get()[0]->user()->get()->pop());
		}
        return $user;
	}
}