
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.admin){window.bootlegger.admin={}};


window.bootlegger.admin.load_module = async function()
{
	await window.bootlegger.core.sysloader('admin');
	// load shit one by one

	// load filestruct root
	const fstruct_root = await window.bootlegger.core.load_dbfile('root.json', 'json');
	$('admin #raid_root_path input').val(fstruct_root['root_path']);

	// load users
	const users = await window.bootlegger.core.py_get(
		{
			'action': 'list_users'
		},
		'json'
	)
	print('loaded users', users)
	// spawn users in GUI
	// todo: this should alctually call add user function and pass login/password
	try {
		for (var usr of users){
			$('admin #userlist').append(`
				<div class="usr_profile">
					<input type="text" class="profile_login" placeholder="Login" value="${usr['login']}">
					<div class="separator">:</div>
					<input type="text" class="profile_pswd" placeholder="Password" value="${usr['pswd']}">
					<img class="userlist_kill_user" draggable="false" src="../assets/rubbish.png">
				</div>
			`);
		}
	} catch (error) {}
	

	//
	// Load allowance list
	//
	window.bootlegger.admin.load_acl_list()

}

window.bootlegger.admin.load_acl_list = async function()
{
	const allowance =  await window.bootlegger.core.py_get(
		{
			'action': 'load_access_list'
		},
		'json'
	)
	$('admin #access_list').empty();

	try {
		print('Spawn allowance list', allowance)
		for (var clr in allowance){
			print('spawn', clr)
			var is_admin = false;
			var clearances = {
				'admin': [],
				'folders': []
			};
			// Admin
			for (var c of allowance[clr]['admin']){
				if (c == 'admin'){
					is_admin = true
					continue
				}
				clearances['admin'].push(`
					<div class="allowance">${c}</div>
				`)
			}
			// Folders
			for (var f of allowance[clr]['folders']){
				clearances['folders'].push(`
					<div class="alw_folderpath_entry">
						<input class="alw_folderpath_input" type="text" value="${f}">
						<img class="alw_kill_folder" draggable="false" src="../assets/rubbish.png">
					</div>
				`)
			}

			$('admin #access_list').append(`
				<div class="usr_allowance">

					<div class="alw_header">
						<div class="alw_header_username">${clr}</div>
						<input ${is_admin ? 'checked' : ''} type="checkbox" class="alw_header_isadmin">
					</div>

					<div class="alw_list_admin">
						<div class="alw_type_header">Permissions:</div>
						<div class="alw_allowance_pool">${clearances['admin'].join('')}</div>
						<btn id="alw_add_admin">Add</btn>
					</div>

					<div class="alw_list_folders">
						<div class="alw_type_header">Folders:</div>
						<div class="alw_folders_pool">${clearances['folders'].join('')}</div>
						<btn id="alw_add_folder">Add</btn>
					</div>

				</div>
			`);
			print('spawnED', clr)
		}
	} catch (error) {
		print(error)
	}
}


// add empty user profile
window.bootlegger.admin.add_user_profile = function()
{
	$('admin #userlist').append(`
		<div class="usr_profile">
			<input type="text" class="profile_login" placeholder="Login">
			<div class="separator">:</div>
			<input type="text" class="profile_pswd" placeholder="Password">
			<img class="userlist_kill_user" draggable="false" src="../assets/rubbish.png">
		</div>
	`);
}


// add empty user profile
window.bootlegger.admin.userlist_kill_user = function(usr)
{
	$(usr).closest('.usr_profile').remove();
}


// duplicate names are not allowed
// takes target input and validates its value against everything else
window.bootlegger.admin.validate_users_nicknames = function(inp)
{
	for (var nick of document.querySelectorAll('admin #userlist .usr_profile input.profile_login')){
		if (nick.value.trim() == inp.value.trim() && nick != inp){
			// print('WHAT?', nick.value.trim(), ':', inp.value.trim())
			inp.style.outlineColor = 'red';
			return
		}
	}

	// if no matches found - remove invalid mark
	inp.style.outlineColor = null;
}


// save user profiles back to server
// keep in mind that pySend does NOT accept objects. Strings and Buffers only (kinda)
window.bootlegger.admin.save_user_profiles = async function()
{
	payload = {};
	for (var usr of document.querySelectorAll('admin #userlist .usr_profile')){
		const nick = $(usr).find('input.profile_login').val();
		const pswd = $(usr).find('input.profile_pswd').val();
		payload[nick] = pswd;
	}

	const do_send = await window.bootlegger.core.py_send(
		{
			'action': 'save_user_profiles'
		},
		JSON.stringify(payload, '\t', 4)
	)

	print('Send result:', do_send)

	window.bootlegger.admin.load_acl_list()

}



window.bootlegger.admin.alw_kill_folder = function(fl)
{
	$(fl).closest('.alw_folderpath_entry').remove()
}




window.bootlegger.admin.add_allowed_folder = function(usr)
{
	$(usr).closest('.alw_list_folders').find('.alw_folders_pool').append(`
		<div class="alw_folderpath_entry">
			<input class="alw_folderpath_input" type="text" value="sandwich">
			<img class="alw_kill_folder" draggable="false" src="../assets/rubbish.png">
		</div>
	`);
}


window.bootlegger.admin.save_allowance_list = async function(usr)
{
	var acl = {};

	for (var entry of document.querySelectorAll('#access_list .usr_allowance')){
		
		// folders
		var get_folders = [];
		for (var fld of entry.querySelectorAll('.alw_folderpath_entry input.alw_folderpath_input')){
			get_folders.push(fld.value.trim().strip('/'))
		}

		// admin
		var get_admin = [];
		for (var adm of entry.querySelectorAll('.alw_list_admin .alw_allowance_pool .allowance')){
			get_admin.push(adm.textContent.trim())
		}
		// stupid ?
		if ($(entry).find('.alw_header_isadmin')[0].checked){
			get_admin.push('admin')
		}


		acl[$(entry).find('.alw_header_username').text().trim()] = {
			'folders': get_folders,
			'admin': get_admin
		}
	}

	const save_response = await window.bootlegger.core.py_send(
		{
			'action': 'save_allowance_list'
		},
		JSON.stringify(acl),
		'text'
	)

	print('Save allowance list:', save_response)
}












