
if (!window.bootlegger){window.bootlegger = {}};

if (!window.bootlegger.ft){window.bootlegger.ft={}};

window.bootlegger.ft.file_upload_q = []
window.bootlegger.ft.lock_queue = false;
// dont forget to lock this after the file upload has started
function file_pool_drop_react(evt)
{
	evt.preventDefault()
	file_pool_drag_leave_react()

	// todo: does it really has to be const?
	const item_list = evt.dataTransfer.items || evt.dataTransfer.files;

	// iterate over shit and add them to the raw queue
	for (var fl of item_list){
		if (window.bootlegger.ft.lock_queue == true){return}
		if (fl.kind && fl.kind == 'file'){
			var getf = fl.getAsFile()
			window.bootlegger.ft.file_upload_q.push({
				'file': getf,
				'processed': false
			})
			$('dlq #dlq_list').append(`<div upl_name="${getf.name}" class="dlq_item">${getf.name}</div>`)
		}
		if (!fl.kind){
			window.bootlegger.ft.file_upload_q.push({
				'file': fl,
				'processed': false
			})
			$('dlq #dlq_list').append(`<div upl_name="${fl.name}" class="dlq_item">${fl.name}</div>`)
		}
	}

	window.bootlegger.ft.process_upload_queue()
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


window.bootlegger.ft.get_file_slice = async function(file, slice_arr)
{
	return new Promise(function(resolve, reject){
		var reader = new FileReader();
	    reader.readAsArrayBuffer(file.slice(slice_arr[0], slice_arr[1]), 'UTF-8');
	    reader.onload = function (evt) {
	    	// convert read result to blob
			resolve(reader.result)
		};
	});
}

window.bootlegger.ft.img_preview_cache = {}
// upload items one by one
window.bootlegger.ft.process_upload_queue = async function()
{
	if (window.bootlegger.ft.lock_queue == true){return}
	window.bootlegger.ft.lock_queue = true;
	// dont tell anyone, but for now it's super raw
	const server_dir_path = `${window.league}/${window.league_match}/${window.struct_fld}`
	for (var upl in window.bootlegger.ft.file_upload_q){
		if (window.bootlegger.ft.file_upload_q[upl]['processed'] == true){continue}

		const thefile = window.bootlegger.ft.file_upload_q[upl]['file']
		const flname = thefile.name
		const flsize = thefile.size
		const server_file_path = `${server_dir_path}/${flname}`
		window.bootlegger.ft.killme = flsize

		print('filebytes length', flsize)
		window.localStorage.setItem('q_break_name', flname)

		// LFS
		if (flsize >= ((1024**2)*256)){
			$(`dlq #dlq_list .dlq_item[upl_name="${flname}"]`).remove()
			$('dlq #dlq_list').append(`
				<div flpath="${server_file_path}" class="dlq_item lfs_item">
					<div class="lfs_item_name">${flname}</div>
					<div class="lfs_progress"></div>
				</div>`);
			// init lfs
			const lfs_init = await window.bootlegger.core.py_get(
				{
					'action': 'upload_sys.lfs_create',
					'file_dest': server_file_path,
					'flname': flname
				},
				'json'
			)
			print(lfs_init)
			if (lfs_init['status'] != 'ok'){
				$(`dlq #dlq_list .dlq_item.lfs_item[flpath="${server_file_path}"]`).addClass('rejected_upload')
				continue
			}

			// keep sending shit
			var offs = 0;
			// const chunk_size = (1024**2)*2
			const chunk_size = (1024**2)*5
			while (true){
				var fl_slice = await window.bootlegger.ft.get_file_slice(thefile, [offs, offs+chunk_size])
				if (fl_slice.byteLength <= 0){break}
				var chunk_append = await window.bootlegger.core.py_send(
					{
						'action': 'upload_sys.lfs_append',
						'target': lfs_init['target']
					},
					fl_slice,
					'json'
				)
				offs += chunk_size
				window.localStorage.setItem('q_break_offs', offs)
				print(chunk_append, 'Offset:', offs, 'Total', flsize, 'perc', offs/flsize)
				$(`dlq #dlq_list .dlq_item.lfs_item[flpath="${server_file_path}"] .lfs_progress`).css('transform', `scaleX(${offs/flsize})`)
			}

			const close_lfs = await window.bootlegger.core.py_get(
				{
					'action': 'upload_sys.lfs_collapse',
					'tgt_dir': server_dir_path,
					'src_lfs': lfs_init['target']
				},
				'json'
			)
			$(`dlq #dlq_list .dlq_item.lfs_item[flpath="${server_file_path}"]`).remove()
			print(close_lfs)
			// await window.bootlegger.main_pool.temp_lies(`${window.bootlegger.core.fsys_root}/${server_file_path}`)
			await window.bootlegger.main_pool.list_media(null, window.struct_fld)
			window.localStorage.removeItem('q_break_name')
			continue
		}

		// else - not LFS
		const upl_response =  await window.bootlegger.core.py_send(
			{
				'action': 'upload_sys.tmp_upload_file',
				'dest': server_file_path
			},
			(await window.bootlegger.core.file_to_bytes(thefile)),
			'json'
		)
		print(upl_response)
		if (upl_response['status'] != 'lizard'){
			$(`dlq #dlq_list .dlq_item[upl_name="${flname}"]`).addClass('rejected_upload')
			continue
			// return
		}
		$(`dlq #dlq_list .dlq_item[upl_name="${flname}"]`).addClass('processed_upload')
		await window.bootlegger.main_pool.temp_lies(`${window.bootlegger.core.fsys_root}/${server_file_path}`)
		window.bootlegger.ft.file_upload_q[upl]['processed'] = true
	}
	window.bootlegger.ft.lock_queue = false;
	window.bootlegger.ft.file_upload_q = []
	$(`dlq #dlq_list .dlq_item[upl_name]`).remove()
	$(`dlq #dlq_list .dlq_item.lfs_item`).remove()

}




window.bootlegger.ft.process_download_queue_old = async function()
{
	const zip = new JSZip();

	// zip.file("Hello.txt", "Hello World\n");

	// const img = zip.folder("images");
	// img.file("smile.gif", imgData, {base64: true});

	for (var dl_med of window.bootlegger.main_pool.media_selection){
		if (!dl_med){continue}
		// todo: check for cache ?
		const media_buffer = await window.bootlegger.core.py_get(
			{
				'action': 'poolsys.load_fullres_pic',
				'target': dl_med
			},
			'buffer'
		)
		zip.file(dl_med.split('/').at(-1), media_buffer);
		$(`mpool dlq #dlq_list .dlq_item[media_path="${dl_med}"]`).addClass('dlq_item_processed');
	}

	// use await
	zip.generateAsync({type:'blob', streamFiles: true}).then(function(content) {
		// see FileSaver.js
		print('generated archive')
		saveAs(content, 'photos.zip');
		$(`mpool dlq #dlq_list .dlq_item`).remove();
		$('flist-entry').removeClass('media_entry_selected');
		window.bootlegger.main_pool.media_selection = [];
	});

}


window.bootlegger.ft.process_download_queue = async function()
{
	// const zip = new JSZip();

	// zip.file("Hello.txt", "Hello World\n");

	// const img = zip.folder("images");
	// img.file("smile.gif", imgData, {base64: true});
	pld = []
	for (var dl_med of window.bootlegger.main_pool.media_selection){
		// pld.push(dl_med.getAttrbute('flpath'))
	}
	const dl_link = await window.bootlegger.core.py_send_fuck(
		{
			'action': 'gen_file',
		},
		JSON.stringify(window.bootlegger.main_pool.media_selection, '\t', 4),
		'text'
	)
	print('got dl filename', dl_link)
	var element = $('<a download="photos.zip"></a>');
	element.attr('href', `htbin/zip_dl.py?action=give_file&dlink=${dl_link}`);
	// element.style.display = 'none';
	// document.body.append('append');
	element[0].click();
	element.remove();
	// zip.file(dl_med.split('/').at(-1), media_buffer);
	// $(`mpool dlq #dlq_list .dlq_item[media_path="${dl_med}"]`).addClass('dlq_item_processed');
	$(`mpool dlq #dlq_list .dlq_item`).remove();
	$('flist-entry').removeClass('media_entry_selected');
	window.bootlegger.main_pool.media_selection = [];
}


