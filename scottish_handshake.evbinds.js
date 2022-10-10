document.addEventListener('click', tr_event => {


	// ==========================================
	// 	sys_chooser syschoser
	// ==========================================

	if (event.target.closest('syschoose #sysc_vids')){window.bootlegger.vidman.load_module()}




	// ==========================================
	// 	vidman vidman
	// ==========================================

	if (event.target.closest('vman_admin #vma_add_pool_src')){window.bootlegger.vidman.add_src_pool_entry()}
	if (event.target.closest('vman_admin .srcs_pool_entry img')){window.bootlegger.vidman.del_src_pool_entry(event.target.closest('vman_admin .srcs_pool_entry img'))}
	if (event.target.closest('vman_admin #vma_save_sources')){window.bootlegger.vidman.save_vid_pool_srcs()}


});


