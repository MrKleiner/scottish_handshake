





$this.load_module = async function()
{
	await $all.core.sysloader('login');
}


$this.intrusion = async function()
{
	const try_login = JSON.parse(await $all.core.py_get(
		'gateway.py',
		{
			'action': 'login',
			'password': $('login #login_pswd').val(),
			'username': $('login #login_username').val()
		}
	))


	// if received token - reload
	if (try_login['token']){
		print(try_login)
		window.localStorage.setItem('auth_token', try_login['token'])
		window.location.reload()
	}else{
		$('login #login_box input').css('outline-color', 'red');
	}
}




$this.logout = function()
{
	window.localStorage.removeItem('auth_token');
	window.location.reload();
}
