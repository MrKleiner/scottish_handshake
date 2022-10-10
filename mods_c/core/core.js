
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.core){window.bootlegger.core={}};

// remappings
window.print = console.log;

// important notes:
// preview indexing works as follows:
// a bunch of binaries (webp) where every name is sha256 of the path in the RAID pool

// dev temp
window.localStorage.setItem('auth_token', '23849e61d01d323826345f22d6e0b3040d87b8c9d24ef7ad122ec805adac3590');


// load a specified system
// does nothing if no system specified
window.bootlegger.core.sysloader = async function(sysname=null)
{
	// dont bother if invalid
	if (!sysname){
		print('Invalid system name:', sysname);
	};

	// start loading...
	return new Promise(function(resolve, reject){
		fetch(`panels/${sysname}.html`, {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			},
			'method': 'GET',
			'mode': 'cors',
			'credentials': 'omit'
		})
		.then(function(response) {
			// print(response.status);
			if (response.status == 404){
				print('Failed to load a panael', 'Reason:', 'File cannot be found on server');
				resolve({'ok': false, 'reason': 'invalid_url'})
				return
			}
			response.text().then(function(data) {
				print('Found requested panel on server, loading...', sysname, data)
				document.querySelector('#pages_pool').innerHTML = data;
				resolve(true)
			});
		});
	});
}



$(document).ready(function(){
	window.bootlegger.core.sysloader('sys_chooser');
	window.bootlegger.core.profiler();
});


window.bootlegger.core.py_get = async function(md=null, prms={})
{
	print('do py get')
	prms['auth'] = window.localStorage.getItem('auth_token') || 'ftp';

	const urlParams = new URLSearchParams(prms);

	// exec...
	return new Promise(function(resolve, reject){
		fetch(`htbin/${md}?${urlParams.toString()}`, {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			},
			'method': 'GET',
			'mode': 'cors',
			'credentials': 'omit'
		})
		.then(function(response) {
			// print(response.status);
			if (response.status == 404){
				print('Failed to execute py get request');
				// resolve({'ok': false, 'reason': 'invalid_url'})
				return
			}
			response.text().then(function(data) {
				print('Pytalk get request success')
				resolve(data)
			});
		});
	});
}




window.bootlegger.core.py_send = async function(md=null, prms={}, payload='')
{
	prms['auth'] = window.localStorage.getItem('auth_token') || 'ftp';

	const urlParams = new URLSearchParams(prms);

	const pl = new Blob([payload], {type: 'text/plain'});

	// exec...
	return new Promise(function(resolve, reject){
		fetch(`htbin/${md}?${urlParams.toString()}`, {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			},
			'method': 'POST',
			'body': pl,
			'mode': 'cors',
			'credentials': 'omit'
		})
		.then(function(response) {
			// print(response.status);
			if (response.status == 404){
				print('Failed to execute py POST request');
				// resolve({'ok': false, 'reason': 'invalid_url'})
				return
			}
			response.text().then(function(data) {
				print('Pytalk POST request success')
				resolve(data)
			});
		});
	});
}


// determine whether the user is logged in or not
window.bootlegger.core.profiler = function()
{
	if (window.localStorage.getItem('auth_token')){
		$('body').attr('logged_in', true)
	}
}

