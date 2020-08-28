# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Flexpart(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = ""
    git      = 'git@github.com:cosunae/flexpart.git'
    maintainers = ['cosunae']

    version('cosmo1-e', branch='empa-prerel-aws')
    
    depends_on('netcdf-fortran~mpi')
    depends_on('netcdf-c~mpi')
    depends_on('cosmo-grib-api')

    build_directory = 'src'

    def build(self, spec, prefix):
        with working_dir(self.build_directory):

          print("PPP")
          make('-f', 'Makefile.ubuntu')
          print("EEE")
    def install(self, spec, prefix): 
        mkdir(prefix.bin)
        install('bin/FLEXPART', prefix.bin)

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile.ubuntu')
            makefile.filter('FFLAGS *:=.*','FFLAGS := -I{0}/include -I{1}/include'.format(spec['netcdf-fortran'].prefix, spec['cosmo-grib-api'].prefix))

