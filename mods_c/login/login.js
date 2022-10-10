
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.login){window.bootlegger.login={}};






window.bootlegger.login.load_module = async function()
{
	await window.bootlegger.core.sysloader('login');
}


window.bootlegger.login.intrusion = async function()
{
	const try_login = JSON.parse(await window.bootlegger.core.py_get(
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




window.bootlegger.login.logout = function()
{
	window.localStorage.removeItem('auth_token');
	window.location.reload();
}
