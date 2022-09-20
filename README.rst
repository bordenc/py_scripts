================
 Python Scripts
================

Introduction
============

I'm self-learning Python. As should be obvious, I'm still very amateur. This is where I dump scripts that I wrote to do odd jobs on my computer where I couldn't find suitable code to copy. The purpose of this repo is:

1. Help others who have similar problems not reinvent the proverbial wheel;
2. Solicit feedback and criticism on my code style. It would be great if some of these evolved into useful utilities; and
3. Practise using git.

Except where noted, scripts are independent of one another. That is, you can use one script without any others in this repo.

Scripts are minimally tested (happy for feedback there, too), and run on `Debian testing <https://packages.debian.org/testing/python/>`_ with its python libraries. Non-Debian libraries have been imported from pip.

Repo contents
=============

`bocfx.py <https://github.com/bordenc/py_scripts/blob/main/bocfx.py>`_
----------------------------------------------------------------------

Retrieves currency exchange rates from the `Bank of Canada <https://www.bankofcanada.ca/valet/docs>`_. For a single date, returns a ``decimal.Decimal`` with the rate. For a date range, returns a dict with key=date and value=rate. This helps me when doing tax returns and I need to convert into CAD.

TO DO
~~~~~

1. On weekends and stat holidays, the script returns an empty dictionary. `CRA advises <https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios-index/series-5-international-residency/series-5-international-residency-folio-4-foreign-currency/income-tax-folio-s5-f4-c1-income-tax-reporting-currency.html>`_ that the "correct" rate is the one from "the closest preceding day for which such a rate is quoted." Therefore, the script should have a way of detecting weekends and stat holidays and quote the "closest preceding day."
2. A cache would be nice to avoid belabouring our good friends at the Bank of Canada with repetitive API calls

`monitorsize.py <https://github.com/bordenc/py_scripts/blob/main/monitorsize.py>`_
----------------------------------------------------------------------------------

*Very* trivial script I created when figuring out which monitors would fill a space. Consists of two functions:

- ``width_to_diagonal_height`` takes the monitor resolution (x & y) and the width and derives the monitor (measured diagonally) that'll fit into that space with the the height it'll occupy
- ``diagonal_to_x_y`` takes the monitor resolution (x & y), the diagonal size (as advertised) and returns the height and width of that monitor.

It's a stupid script but included here for anyone who needs to double-check that they solved the Pythagorean Theorem correctly... which I hope is nobody over the age of twelve if you're reading this.

`rename_files_from_contents.py <https://github.com/bordenc/py_scripts/blob/main/rename_files_from_contents.py>`_
----------------------------------------------------------------------------------------------------------------

Selects all files in a single directory (I decided not to use ``os.walk()`` to increase safety) that match some regular expression and then renames those files based on the results of the first regular expression match in some part of that file. For example:

::

	file_name_match_pattern = r'.+\.vcf'
	in_file_match_pattern = r'FN:(.+)\n'
	base_directory = '/home/user/vCards/'

Would rename all of the `.vcf` files in a directory to the contents of the file's formatted name (``FN:``).

TO DO
~~~~~

1. The file currently doesn't preserve the file extension/suffix. So, in the example above, ``123.vcf`` would be renamed to ``Jane Doe`` (no extension). I'm trying to think of the least hacky way of doing this without invoking another regex or calling the ``pathlib.Path``. Suggestions welcome.
2. An elegant way of specifying a renaming pattern with multiple group matches would be nice, so a pattern ``FN:(\w+) (\w+)`` could turn into ``\2_\1.vcf``
3. I'm sure the script is all sorts of fragile and will break at the first error. Again, feedback welcome.