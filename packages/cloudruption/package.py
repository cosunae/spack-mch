# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Cloudruption(CMakePackage):
    """toy model to test messaging communication of services in the cloud"""

    homepage = 'https://github.com/cosunae/cloudruption'
    git = 'https://github.com/cosunae/cloudruption.git'

    maintainers = ['cosunae']
    
    version('master', git='https://github.com/cosunae/cloudruption.git', branch='master' )

    variant('enable_producer', default=True,
            description='Enable Producer')
    variant('enable_mpi', default=True,
            description='Enable MPI')
    variant('enable_fortran', default=True,
            description='Enable Fortran')

    depends_on('mpi')
    depends_on('eccodes')

    # Can be built with Python2 or Python3.
#    depends_on('python@3.6:', type='build')
#    depends_on('py-numpy', type=('build', 'run'))
#    extends('python', when='+python')

    root_cmakelists_dir='ProducerConsumer'

    def cmake_args(self):
        args = ['-DENABLE_PRODUCER=ON' ]

        return args
