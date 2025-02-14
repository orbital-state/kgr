db:
	[ -d var ] || mkdir -p var
	sqlite3 var/log.sqlite "CREATE TABLE actions (id INTEGER PRIMARY KEY, manifest TEXT, action_name TEXT, parameters TEXT);"