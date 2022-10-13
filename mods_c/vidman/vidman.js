
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.vidman){window.bootlegger.vidman={}};


// There's little to no time to document this rubbish properly,
// so explanation does here:
// For the whole system to work, you have to specify root folders of stream systems
// It's assumed that a single stream system is structured like "SYSNAME"/"streams"/"VIDEO FILES"
// each time someone calls for the video pool - these folders are scanned for videos
// and returned to js with a raw filename alongside its PRESUMABLE preview ID

// js does some shit and it's pointless to explain it further

// this panel is responsible for managing these root folders...
// add, remove, read...


window.bootlegger.vidman.load_module = async function ()
{
	await window.bootlegger.core.sysloader('vidman');
	// display folders
	const folders = JSON.parse(
		await window.bootlegger.core.py_get(
			'gateway.py',
			{
				'action': 'get_vid_pool_paths'
			}
		)
	)
	
	// append the folders
	const pool_entries = $('vidman #tree_pool_entries');
	for (var fld of folders){
		pool_entries.append(`
			<div fullpath="${fld.path}" class="entry_folder">${fld.name}</div>
		`)
	}
}

window.bootlegger.vidman.load_admin = async function ()
{
	await window.bootlegger.core.sysloader('vidman_admin');
	window.bootlegger.vidman.load_vid_pool_srcs()
}


// load paths from where to get videos from
// important: strict format:
// cityname.date.time.extension
window.bootlegger.vidman.load_vid_pool_srcs = async function()
{
	const pool = JSON.parse(
		await window.bootlegger.core.py_get('gateway.py', {
			'action': 'get_vid_pool_paths'
		})
	)

	var spool = $('vman_admin #vma_srcs_pool');
	for (var src_entry of pool){
		spool.prepend(`
			<div class="srcs_pool_entry">
				<input class="display_name" placeholder="Display Name" type="text" value="${src_entry.name}">
				<div class="pool_entry_separator">:</div>
				<input class="full_path" placeholder="Full Path (absolute)" type="text" value="${src_entry.path}">
				<img draggable="false" src="../assets/rubbish.png">
			</div>
		`)
	}
}


// load paths from where to get videos from
// important: strict format:
// cityname.date.time.extension
window.bootlegger.vidman.save_vid_pool_srcs = async function()
{
	var srcs_entries = [];

	for (var en of document.querySelectorAll('vman_admin .srcs_pool_entry')){
		srcs_entries.push({
			'name': en.querySelector('input.display_name').value,
			'path': en.querySelector('input.full_path').value
		});
	}

	const dosave = await window.bootlegger.core.py_send(
		'gateway.py',
		{'action': 'upd_vid_pool_paths'},
		JSON.stringify(srcs_entries)
	)

	// print('KILL NME ')
}




window.bootlegger.vidman.add_src_pool_entry = function()
{
	$('vman_admin #vma_srcs_pool').prepend(`
		<div class="srcs_pool_entry">
			<input class="display_name" placeholder="Display Name" type="text">
			<div class="pool_entry_separator">:</div>
			<input class="full_path" placeholder="Full Path (absolute)" type="text" value="/raid">
			<img draggable="false" src="../assets/rubbish.png">
		</div>
	`)
}


window.bootlegger.vidman.del_src_pool_entry = function(elem)
{
	$(elem).closest('.srcs_pool_entry').remove();
}


window.bootlegger.vidman.list_vids = async function(etgt)
{
	const vids_list = JSON.parse(
		await window.bootlegger.core.py_get('gateway.py', {
			'action': 'vdman_list_pool',
			'fld_path': etgt.getAttribute('fullpath')
		})
	)

	print(vids_list)

	window.preview_queue = [];

	$('vidman #content_pool #content_pool_vids').empty();

	for (var vid of vids_list){
		var vid_e = $(`
			<div class="vid_entry" vidpath="${vid.path}">
				<div class="vid_entry_preview"></div>
				<div class="vid_entry_caption">${vid.name}</div>
			</div>
		`)

		$('vidman #content_pool #content_pool_vids').append(vid_e)

		window.preview_queue.push({
			'vidpath': vid.path,
			'elem': vid_e
		})
	}
}



