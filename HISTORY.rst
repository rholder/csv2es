.. :changelog:

History
-------

1.0.2 (2016-01-17)
++++++++++++++++++
- Fix when neither --delimiter nor --tab is provided. New default: ','.
- Added *~ to .gitignore

1.0.1 (2015-06-02)
++++++++++++++++++
- Add option to stream from stdin

1.0.0 (2015-04-23)
++++++++++++++++++
- Add retrying support with exponential backoff per chunk for bulk uploads
- Add parallel bulk uploading via joblib
- Stable release

1.0.0.dev3 (2015-04-19)
+++++++++++++++++++++++
- Switch over to Click for handling executable
- Fix --delete-index flag
- Add --version option

1.0.0.dev2 (2015-04-19)
+++++++++++++++++++++++
- Fix import errors

1.0.0.dev1 (2015-04-18)
+++++++++++++++++++++++
- Tinkering with documentation and PyPI updates

1.0.0.dev0 (2015-04-18)
+++++++++++++++++++++++
- First dev version now exists
- Apache 2.0 license applied
- Finalize commandline interface
- Sanitizing some setup.py and test suite running
- Added Travis CI support
