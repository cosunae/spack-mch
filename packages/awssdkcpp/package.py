# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Awssdkcpp(CMakePackage):
    """toy model to test messaging communication of services in the cloud"""

    homepage = 'https://github.com/cosunae/cloudruption'
    git = 'https://github.com/aws/aws-sdk-cpp'

    maintainers = ['cosunae']
    
    version('master', git='https://github.com/aws/aws-sdk-cpp', branch='master' )
    patch('patches/patch.master')

    # the patch was extracted with hash 87a84561fb46fbcb8efe502f6070533a5372a46a
