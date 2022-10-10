

// There's little to no time to document this rubbish properly,
// so explanation does here:
// For the whole system to work, you have to specify root folders of stream systems
// It's assumed that a single stream system is structured like "SYSNAME"/"streams"/"VIDEO FILES"
// each time someone calls for the video pool - these folders are scanned for videos
// and returned to js with a raw filename alongside its PRESUMABLE preview ID

// js does some shit and it's pointless to explain it further

// this panel is responsible for managing these root folders...
// add, remove, read...


$this.load_module = async function ()
{
	await $all.core.sysloader('vidman_admin');
	$this.load_vid_pool_srcs()
}


// load paths from where to get videos from
// important: strict format:
// cityname.date.time.extension
$this.load_vid_pool_srcs = async function()
{
	const pool = JSON.parse(
		await $all.core.py_get('gateway.py', {
			'action': 'get_vid_pool_paths'
		})
	)

	var spool = $('vman_admin #vma_srcs_pool');
	for (var src_entry of pool){
		spool.prepend(`
			<div class="srcs_pool_entry">
				<input type="text" value="${src_entry}">
				<img draggable="false" src="../assets/rubbish.png">
			</div>
		`)
	}
}


// load paths from where to get videos from
// important: strict format:
// cityname.date.time.extension
$this.save_vid_pool_srcs = async function()
{
	var srcs_entries = [];

	for (var en of document.querySelectorAll('vman_admin .srcs_pool_entry input')){
		srcs_entries.push(en.value);
	}

	const dosave = await $all.core.py_send(
		'gateway.py',
		{'action': 'upd_vid_pool_paths'},
		JSON.stringify(srcs_entries)
	)

	// print('KILL NME ')
}




$this.add_src_pool_entry = function()
{
	$('vman_admin #vma_srcs_pool').prepend(`
		<div class="srcs_pool_entry">
			<input draggable="false" type="text" value="/raid">
			<img draggable="false" src="../assets/rubbish.png">
		</div>
	`)
}


$this.del_src_pool_entry = function(elem)
{
	$(elem).closest('.srcs_pool_entry').remove();
}






