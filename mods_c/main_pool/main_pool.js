
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.main_pool){window.bootlegger.main_pool={}};




window.bootlegger.main_pool.module_loader = async function()
{
	await window.bootlegger.core.sysloader('main_pool');

	// list root shite
	const roots = await window.bootlegger.core.py_get(
		{
			'action': 'list_root_shite'
		},
		'json'
	)
	// spawn shite
	for (var entry of roots){
		$('mpool flist').append(`
			<fld class="rootf" fldname="${entry}">
				<etype>
					<div clas="etype_folder"></div>
				</etype>
				<ename>${entry}</ename>
			</fld>
		`)
	}

}