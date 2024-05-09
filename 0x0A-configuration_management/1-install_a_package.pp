<<<<<<< HEAD
#!/usr/bin/pup
# Installs flask from pip3, version 2.1.0
=======
##!/usr/bin/pup
# 1-install_a_package.pp
>>>>>>> bdddb161737a53e26ab3d5fa30724da24befba4f

package { 'flask':
  ensure   => '2.1.0',
  provider => 'pip3'
}

