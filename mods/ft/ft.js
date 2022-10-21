
$this.file_upload_q = []

// dont forget to lock this after the file upload has started
function file_pool_drop_react(evt)
{
	evt.preventDefault()
	file_pool_drag_leave_react()

	// todo: does it really has to be const?
	const item_list = evt.dataTransfer.items || evt.dataTransfer.files;

	// iterate over shit and add them to the raw queue
	for (var fl of item_list){
		if (fl.kind && fl.kind == 'file'){
			$this.file_upload_q.push({
				'file': fl.getAsFile(),
				'processed': false
			})
		}
		if (!fl.kind){
			$this.file_upload_q.push({
				'file': fl,
				'processed': false
			})
		}
	}

	$this.process_upload_queue()
}


// this is needed to prevent browser from opening dragged files
// YES, this has to be done when the drop has just starter and NOT when released...
// it appears that preventDefault has to be EVERYWHERE
function file_pool_hover_react(evt)
{
	evt.preventDefault();
}

function file_pool_drag_enter_react()
{
	$('body').prepend(`
		<div id="indicate_can_drop_files">
			<div id="indicate_can_drop_files_icon"></div>
		</div>
	`)
}

function file_pool_drag_leave_react()
{
	$('#indicate_can_drop_files').remove();
}


// upload items one by one
$this.process_upload_queue = async function()
{
	// dont tell anyone, but for now it's super raw
	for (var upl in $this.file_upload_q){
		if ($this.file_upload_q[upl]['processed'] == true){continue}
		const upl_response =  await $all.core.py_send(
			{
				'action': 'upload_sys.tmp_upload_file',
				'dest': `${window.league}/${window.league_match}/${window.struct_fld}/${$this.file_upload_q[upl]['file'].name}`
			},
			(await $all.core.file_to_bytes($this.file_upload_q[upl]['file'])),
			'json'
		)
		print(upl_response)
		if (upl_response['status'] != 'lizard'){return}
		await $all.main_pool.temp_lies(`${$all.core.fsys_root}/${window.league}/${window.league_match}/${window.struct_fld}/${$this.file_upload_q[upl]['file'].name}`)
		$this.file_upload_q[upl]['processed'] = true
	}

}









