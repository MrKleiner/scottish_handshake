



$this.module_loader = async function()
{
	await $all.core.sysloader('main_pool');

	// list root shite
	const roots = await $all.core.py_get(
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