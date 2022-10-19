
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.core){window.bootlegger.core={}};

// remappings
window.print = console.log;

// important notes:
// preview indexing works as follows:
// a bunch of binaries (webp) where every name is sha256 of the path in the RAID pool

// dev temp
// window.localStorage.setItem('auth_token', '23849e61d01d323826345f22d6e0b3040d87b8c9d24ef7ad122ec805adac3590');



//
// presumable video preview / meta format:
//

// gigabin

// -----------------------------
// gigabin struct specification:
// -----------------------------

// First 7 bytes are strictly dedicated to the file format indication,
// aka first 7 bytes are a string "gigabin"

// Following 32 bytes are dedicated to the header size of the file in bytes
// any unused space out of these 32 bytes is padded with !

// Header is stored in the end of the entire file,
// allowing modification of the content without rewriting the entire file

// Header is a json encoded with Base64
// Header format:
// {
// 	'stores': {
// 		'filename': {
// 			'type': 'solid',
// 			'bits': [OFFSET_BYTES, LENGTH_BYTES, 'sha256 hash or null']
// 		},
// 		'filename2': [
// 			'type': 'array',
// 			'bits': [
// 				[OFFSET_BYTES, LENGTH_BYTES, 'sha256 hash or null'],
// 				[OFFSET_BYTES, LENGTH_BYTES, 'sha256 hash or null']
// 				...
// 			]
// 		]
// 	},
// 	'version': gigabin_version, like 0.7,
//	'total_size': 1 or null, (null by default)
// 	'comment': ''
// }

// sha256 is null by default in both libraries

// The rest of the file is a continous dump of bytes

// gigabin is available as a library for javascript and python
// The python version is the most efficient, since the entire fine doesn't has to be read








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
	window.bootlegger.main_pool.module_loader();
	window.bootlegger.core.profiler();
});


// prms: URL parameters to pass to the CGI script
// as: treat response as text/json/buffer
// returns json with response status and payload
window.bootlegger.core.py_get = async function(prms={}, load_as='text')
{
	print('Exec PY get')

	// add auth token to the request
	prms['auth'] = window.localStorage.getItem('auth_token') || 'ftp';

	// convert payload to URL params
	const urlParams = new URLSearchParams(prms);

	// exec...
	return new Promise(function(resolve, reject){
		fetch(`htbin/gateway.py?${urlParams.toString()}`, {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			},
			'method': 'GET',
			'mode': 'cors',
			'credentials': 'omit'
		})
		.then(async function(response) {
			// print(response.status);
			if (response.status == 404){
				print('Failed to execute py get request');
				return
			}

			// honestly, FUCKOFF
			// this is just fine
			const bin = new Uint8Array(await response.arrayBuffer())

			// todo: for now use try catch
			// come up with something adequate later....
			try {
				if (load_as == 'text'){
					resolve(lizard.UTF8ArrToStr(bin))
					return
				}
				if (load_as == 'json'){
					resolve(JSON.parse(lizard.UTF8ArrToStr(bin)))
					return
				}
				if (load_as == 'buffer'){
					resolve(bin)
					return
				}
				if (load_as == 'blob'){
					const boobs = new Blob([bin], {});
					resolve(boobs)
					return
				}
				if (load_as == 'blob_url'){
					const boobs = new Blob([bin], {});
					resolve((window.URL || window.webkitURL).createObjectURL(boobs))
					return
				}
				console.warn('PyGet Warn: falling back to default data type');
				resolve(lizard.UTF8ArrToStr(bin))

			} catch (error) {
				console.warn('PyGet Error', lizard.UTF8ArrToStr(bin))
			}

		});
	});
}



// prms: URL parameters to pass to the CGI script
// payload: payload to send. Has to be proper shit and not raw objects
// as: treat response as text/json/buffer
window.bootlegger.core.py_send = async function(prms={}, payload='', as='text')
{
	// add auth token to the payload
	prms['auth'] = window.localStorage.getItem('auth_token') || 'ftp';

	// convert params to URL params
	const urlParams = new URLSearchParams(prms);

	// convert payload to BLOB
	const pl = new Blob([payload], {type: 'text/plain'});

	// exec...
	return new Promise(function(resolve, reject){
		fetch(`htbin/gateway.py?${urlParams.toString()}`, {
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
		.then(async function(response) {
			// print(response.status);
			if (response.status == 404){
				print('Failed to execute py SEND request');
				return
			}

			// honestly, FUCKOFF
			// this is just fine
			const bin = new Uint8Array(await response.arrayBuffer())

			// todo: for now use try catch
			// come up with something adequate later....
			try {
				if (load_as == 'text'){
					resolve(lizard.UTF8ArrToStr(bin))
					return
				}
				if (load_as == 'json'){
					resolve(JSON.parse(lizard.UTF8ArrToStr(bin)))
					return
				}
				if (load_as == 'buffer'){
					resolve(bin)
					return
				}
				console.warn('PyGet Warn: falling back to default data type');
				resolve(lizard.UTF8ArrToStr(bin))

			} catch (error) {
				console.warn('PyGet Error', lizard.UTF8ArrToStr(bin), error)
			}

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



window.bootlegger.core.load_dbfile = function(flpath, load_as)
{
	return new Promise(function(resolve, reject){
		fetch(`db/${flpath.strip('/')}`, {
			'headers': {
				'accept': '*/*',
				'cache-control': 'no-cache',
				'pragma': 'no-cache'
			},
			'method': 'GET',
			'mode': 'cors',
			'credentials': 'omit'
		})
		.then(async function(response) {
			// console.log(response.status);
			if (response.status == 404){
				resolve('DB File load: File does not exist')
				return
			}

			// todo: Just use response[GET AS]
			// and require this function to take proper read as statements

			// TEXT
			if (load_as == 'text'){
				resolve(await response.text())
				return
			}

			// JSON
			if (load_as == 'json'){
				resolve(await response.json())
				return
			}

			// buffer
			if (load_as == 'buffer'){
				resolve(await response.arrayBuffer())
				return
			}

			resolve(await response.text())
			return


		});
	});
}

