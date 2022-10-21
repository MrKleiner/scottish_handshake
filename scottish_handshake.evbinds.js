document.addEventListener('input', tr_event => {


	// ==========================================
	// 	admin admin
	// ==========================================

	if (event.target.closest('admin #userlist .usr_profile input.profile_login')){window.bootlegger.admin.validate_users_nicknames(event.target.closest('admin #userlist .usr_profile input.profile_login'))}


});


document.addEventListener('click', tr_event => {


	// ==========================================
	// 	admin admin
	// ==========================================

	if (event.target.closest('admin btn#save_users')){window.bootlegger.admin.save_user_profiles()}
	if (event.target.closest('admin btn#spawn_new_user')){window.bootlegger.admin.add_user_profile()}
	if (event.target.closest('admin .usr_profile .userlist_kill_user')){window.bootlegger.admin.userlist_kill_user(event.target.closest('admin .usr_profile .userlist_kill_user'))}
	if (event.target.closest('admin .alw_list_folders .alw_kill_folder')){window.bootlegger.admin.alw_kill_folder(event.target.closest('admin .alw_list_folders .alw_kill_folder'))}
	if (event.target.closest('admin .alw_list_folders .alw_kill_admin')){window.bootlegger.admin.alw_kill_admin(event.target.closest('admin .alw_list_folders .alw_kill_admin'))}
	if (event.target.closest('admin .alw_add_folder')){window.bootlegger.admin.add_allowed_folder(event.target.closest('admin .alw_add_folder'))}
	if (event.target.closest('admin .alw_add_admin')){window.bootlegger.admin.add_admin_allowance(event.target.closest('admin .alw_add_admin'))}
	if (event.target.closest('admin #save_access_list')){window.bootlegger.admin.save_allowance_list()}




	// ==========================================
	// 	home home
	// ==========================================

	if (event.target.closest('#app_topbar #nav_login')){window.bootlegger.login.load_module()}
	if (event.target.closest('#app_topbar #nav_sign_out')){window.bootlegger.login.logout()}
	if (event.target.closest('#app_topbar #nav_enter_edit')){window.bootlegger.admin.load_module()}
	if (event.target.closest('#app_topbar #nav_go_home')){window.bootlegger.main_pool.module_loader()}




	// ==========================================
	// 	login login
	// ==========================================

	if (event.target.closest('login #intrusion')){window.bootlegger.login.intrusion()}




	// ==========================================
	// 	main_pool main_pool
	// ==========================================

	if (event.target.closest('mpool flist flist-entry.league')){window.bootlegger.main_pool.list_league_matches(event.target.closest('mpool flist flist-entry.league'))}
	if (event.target.closest('mpool flist flist-entry.match')){window.bootlegger.main_pool.list_match_struct(event.target.closest('mpool flist flist-entry.match'))}
	if (event.target.closest('mpool flist flist-entry.struct_entry')){window.bootlegger.main_pool.list_media(event.target.closest('mpool flist flist-entry.struct_entry'))}
	if (event.target.closest('mpool flist flist-entry.media_entry')){window.bootlegger.main_pool.load_fullres_media(event.target.closest('mpool flist flist-entry.media_entry'))}
	if (event.target.closest('img#pic_fullres_preview')){window.bootlegger.main_pool.viewing_fullres = false;$('img#pic_fullres_preview').remove()}




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


document.addEventListener('keydown', tr_event => {


	// ==========================================
	// 	main_pool main_pool
	// ==========================================

	if (event.target.closest('body')){window.bootlegger.main_pool.img_cycle_lr(tr_event, event.target.closest('body'))}


});


