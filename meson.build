project('braus',  
          version: '0.1.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2' ],
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'braus')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'braus.py',
  output: 'braus',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('data')
subdir('src')
subdir('po')
subdir('ui')

meson.add_install_script('build-aux/meson/postinstall.py')