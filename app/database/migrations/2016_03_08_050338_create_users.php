<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateUsers extends Migration {

	/**
	 * Run the migrations.
	 *
	 * @return voidP
	 */
	public function up()
	{
		Schema::create('users', function($table) {
			$table->increments('id');
			$table->integer('identifier');
			$table->string('name');
			$table->integer('profile_pic');
			$table->integer('wristband_id');
			$table->boolean('status');
		});
	}

	/**
	 * Reverse the migrations.
	 *
	 * @return void
	 */
	public function down()
	{
		Schema::drop('users');
	}

}
