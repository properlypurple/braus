message('Compiling resources')

gnome.compile_resources(
  meson.project_name(),
  'gresource.xml',
  gresource_bundle: true,
  install_dir: join_paths(pkgdatadir),
  install: true
)