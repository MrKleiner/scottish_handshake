document.addEventListener('click', tr_event => {


	// ==========================================
	// 	home home
	// ==========================================

	if (event.target.closest('#app_topbar #nav_login')){window.bootlegger.login.load_module()}
	if (event.target.closest('#app_topbar #nav_sign_out')){window.bootlegger.login.logout()}
	if (event.target.closest('#app_topbar #nav_enter_edit')){window.bootlegger.vidman.load_admin()}




	// ==========================================
	// 	login login
	// ==========================================

	if (event.target.closest('login #intrusion')){window.bootlegger.login.intrusion()}




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
	if (event.target.closest('#tree_pool_entries .entry_folder')){window.bootlegger.vidman.list_vids(event.target.closest('#tree_pool_entries .entry_folder'))}


});


