



$this.module_loader = async function()
{
	await $all.core.sysloader('main_pool');

	// list root shite
	const roots = await $all.core.py_get(
		{
			'action': 'poolsys.list_leagues'
		},
		'json'
	)

	print('fuck this shit', roots)

	$('mpool flist').empty();
	// spawn shite
	for (var entry of roots){
		$('mpool flist').append(`
			<fld class="league" fldname="${entry}">
				<etype folder>
				</etype>
				<ename>${entry}</ename>
			</fld>
		`)
	}


}



$this.list_league_matches = async function(elm)
{
	const fld_name = elm.getAttribute('fldname');

	window.league = fld_name;

	const full_root = (await $all.core.load_dbfile('root.json', 'json'))['root_path']

	const subroot_flds = await $all.core.py_get(
		{
			'action': 'poolsys.list_league_matches',
			'league_name': fld_name
		},
		'json'
	)

	$('mpool flist').empty();

	// spawn shite
	for (var entry of subroot_flds){
		$('mpool flist').append(`
			<fld class="match" fldpath="${entry}">
				<etype folder>
				</etype>
				<ename>${entry}</ename>
			</fld>
		`)
	}
	// now prepend go up
	$('mpool flist').prepend(`
		<fld class="match" onclick="$this.module_loader()">
			<etype up>
			</etype>
			<ename>../</ename>
		</fld>
	`)

}


$this.list_match_struct = async function(elm)
{
	const fld_name = elm.getAttribute('fldpath');

	window.league_match = fld_name;

	const dirlisting = await $all.core.py_get(
		{
			'action': 'poolsys.list_match_struct',
			'match_name': `${window.league}/${window.league_match}`
		},
		'json'
	)

	print('listed match:', dirlisting)

	$('mpool flist').empty();

	for (var lst of dirlisting){
		$('mpool flist').append(`
			<fld class="struct_entry" fldpath="${lst}">
				<etype folder>
				</etype>
				<ename>${lst}</ename>
			</fld>
		`)
	}

	// now prepend go up
	$('mpool flist').prepend(`
		<fld fldname="${window.league}" class="subrootf" onclick="$this.list_league_matches(this)">
			<etype up>
			</etype>
			<ename>../</ename>
		</fld>
	`)
}




$this.list_media = async function(elm)
{
	
	const fld_name = elm.getAttribute('fldpath');

	window.struct_fld = fld_name;

	const dirlisting = await $all.core.py_get(
		{
			'action': 'poolsys.list_media',
			'target': `${window.league}/${window.league_match}/${window.struct_fld}`
		},
		'json'
	)

	print('listed media:', dirlisting)

	$('mpool flist').empty();

	$('flist').css('flex-direction', 'row');
	$('flist').css('flex-wrap', 'wrap');

	$('mpool flist').prepend(`
		<fld fldname="${window.league}" class="go_up" onclick="$this.list_league_matches(this)">
			<etype up_media>
			</etype>
			<ename>../</ename>
		</fld>
	`)

	for (var lst of dirlisting){
		console.time('Media Unit')
		// stupid
		// load preview first
		var media_preview = await $all.core.py_get(
			{
				'action': 'poolsys.load_media_preview',
				'media_path': lst['path']
			},
			'blob_url'
		)
		// print(media_preview)
		// return

		var media_entry = $(`
			<med class="media_entry" flpath="${lst['path']}" flname="${lst['flname']}">
				<etype style="background-image: url(${media_preview})" img>
				</etype>
				<ename>${lst['flname']}</ename>
			</med>
		`)

		$('mpool flist').append(media_entry)

		// load preview
		console.timeEnd('Media Unit')

	}

	
}

$this.fm_cache = [];
$this.cache_fullres_media = function(url)
{
	if ($this.fm_cache.length > 16){
		(window.URL || window.webkitURL).revokeObjectURL($this.fm_cache[0])
		$this.fm_cache.shift()
	}
	$this.fm_cache.push(url)
}


$this.load_fullres_media = async function(elm)
{

	// todo: this should work differently, probaly
	if (!elm.classList.contains('media_entry')){return}
	// delete existing preview from the page
	$('body > img#pic_fullres_preview').remove();
	$this.active_fullres_preview_elem = elm;
	$this.viewing_fullres = true;

	// if cache is present - pull from cache immediately
	const cache_attr = elm.getAttribute('img_cache');
	if ($this.fm_cache.includes(cache_attr)){
		$('body').append(`<img id="pic_fullres_preview" src="${cache_attr}">`);
		return
	}

	const media_path = elm.getAttribute('flpath');

	const tgt = $(`
		<img id="pic_fullres_preview" src="../assets/spinning_circle.svg">
	`);

	$('body').append(tgt)

	const fullres = await $all.core.py_get(
		{
			'action': 'poolsys.load_fullres_pic',
			'target': media_path
		},
		'blob_url'
	)

	// print(fullres)

	// update image src with loaded fullres preview
	tgt[0].src = fullres
	// cache the image
	elm.setAttribute('img_cache', fullres)
	$this.cache_fullres_media(fullres)

}


$this.img_cycle_lr = function(arrow, elm)
{
	// todo: this can totally be better
	if (!$this.active_fullres_preview_elem || $this.viewing_fullres != true){return}
	if (arrow.keyCode == 37){
		$this.load_fullres_media($this.active_fullres_preview_elem.previousSibling)
	}
	if (arrow.keyCode == 39){
		$this.load_fullres_media($this.active_fullres_preview_elem.nextSibling)
	}
}

