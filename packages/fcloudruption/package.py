# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Fcloudruption(CMakePackage):
    """Fortran component of the cloudruption: messaging communication of services in the cloud"""

    homepage = 'https://github.com/cosunae/cloudruption'
    git = 'https://github.com/cosunae/cloudruption.git'

    maintainers = ['cosunae']
    
    version('master', git='https://github.com/cosunae/cloudruption.git', branch='master' )

    variant('enable_mpi', default=True,
            description='Enable MPI')

    depends_on('cloudruption%gcc')

    root_cmakelists_dir='ProducerConsumer/Fortran'

    def cmake_args(self):
        args = ['-DENABLE_PRODUCER=ON' ]
        args.append('-DENABLE_MPI=OFF')

        return args
