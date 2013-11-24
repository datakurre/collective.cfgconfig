This is just an experiment of using zope.configuration with cfg-files instead
of zcml-files.

Known issues:

- cfg-syntax requires unique section names, which require inventing
  dummy extra part for each section

- nested directives are not supported
