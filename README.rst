=============
chibi_browser
=============


.. image:: https://img.shields.io/pypi/v/chibi_browser.svg
        :target: https://pypi.python.org/pypi/chibi_browser

.. image:: https://readthedocs.org/projects/chibi-browser/badge/?version=latest
        :target: https://chibi-browser.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Libreria para controllar selenium para mejorar la legibilidad en otros scripts

* Free software: WTFPL
* Documentation: https://chibi-browser.readthedocs.io.

**********
uso basico
**********

Chibi_browser
=============

Preparar una nueva instancia y usarla para navegar y descargar archivos

.. code-block:: python

	from chibi_browser import Chibi_browser
	harvest_moon_rom = Chibi_browser(
		'https://archive.org/details/harvest-moon-ranch-master',
		download_folder=Chibi_temp_path() )
	links = harvest_moon_rom.select( "div.show-all a.boxy-ttl" )
	# buscar el link con el texto "show all" y clickear el boton
	for link in links:
		if link.text.lower().strip() == 'show all':
				link.click()
				break

	# esperar a que cambie la pagina y este visible la tabla de contenido
	harvest_moon_rom.wait( 10 ).until(
		wait_conditions.element.visible.select(
				"table.directory-listing-table" ) )

	# buscar el archivo torrent y hacerle click para descargarlo
	table = harvest_moon_rom.select_one( "table.directory-listing-table" )
	files = table.select( 'a' )
	for f in files:
		if '.torrent' in f.text:
				f.click()

	# esperar a que se descarge el archivo e imprimir los archivos descargados
	time.sleep( 2 )
	for f in harvest_moon_rom.download_folder.ls():
		print( f )
