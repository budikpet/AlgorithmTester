Slouží pro synchronizaci složky LocalShared do složky Shared, což je sdílená složka s host strojem.

Automatické spuštění skriptu:

	Každých X minut:
	Pomocí crontab. Přidat následující:
		--------------------------------------------------------------------------------------------------
		# */5 * * * * echo 'ping' >> /home/petr/Documents/LocalShared/test      # Every 5 min
		# * * * * * echo 'ping' >> /home/petr/Documents/LocalShared/test        # Every 1 min
		
		SHELL=/bin/bash
		#MAILTO=root@example.com        # Set email address where cron job results are sent
		PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
		
		*/15 * * * * /home/petr/Documents/LocalShared/syncRunner/runSync.sh
		-----------------------------------------------------------------------------------------------------------
	
	Před vypnutím:
	1/ Vložit runSharedSync.service do složky /etc/systemd/system.
	2/ Příkaz: sudo systemctl enable runSharedSync.service
	3/ Bude fungovat po 1. nebo 2. vypnutí.
