# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os

import llnl.util.tty as tty

import spack.config
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
from spack.stage import DIYStage
from spack.spec import Spec

description = "Dev-build cosmo and dycore with or without testing."
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '-d', '--source-path', dest='source_path', default=None,
        help="path to source directory. defaults to the current directory")
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="don't try to install dependencies of requested packages")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="do not remove the install prefix if installation fails")
    subparser.add_argument(
        '--skip-patch', action='store_true',
        help="skip patching for the developer build")
    subparser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help="do not display verbose build output while installing")
    subparser.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")
    subparser.add_argument(
        '-t', '--test', type=str, default='ON',
        help="ON or OFF, dev-build with testing")

    arguments.add_common_arguments(subparser, ['spec'])

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def dev_build(self, args):
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    spec = specs[0]
    if not spack.repo.path.exists(spec.name):
        tty.die("No package for '{0}' was found.".format(spec.name),
                "  Use `spack create` to create a new package")

    if not spec.versions.concrete:
        tty.die(
            "spack dev-build spec must have a single, concrete version. "
            "Did you forget a package version number?")

    spec.concretize()

    package = spack.repo.get(spec)

    if package.installed:
        tty.error("Already installed in %s" % package.prefix)
        tty.msg("Uninstall or try adding a version suffix for this dev build.")
        sys.exit(1)

    source_path = args.source_path
    if source_path is None:
        source_path = os.getcwd()
    source_path = os.path.abspath(source_path)

    # Forces the build to run out of the current directory.
    package.stage = DIYStage(source_path)

    # disable checksumming if requested
    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    package.do_install(
        make_jobs=args.jobs,
        keep_prefix=args.keep_prefix,
        install_deps=not args.ignore_deps,
        verbose=not args.quiet,
        keep_stage=True,   # don't remove source dir for dev build.
        dirty=args.dirty,
        stop_at=args.until)
  
def dev_build_cosmo(self, args):
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    # extract cosmo_spec
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = specs[0]
    cosmo_spec.concretize()

    dycore_spec = 'cosmo-dycore@dev-build'
    cosmo_serialize_spec='cosmo@master%pgi cosmo_target=cpu +serialize ~cppdycore'

    if cosmo_spec.satisfies('real_type=float'):
        real_type='float'
        dycore_spec += ' real_type=' + real_type
        cosmo_serialize_spec += ' real_type=' + real_type

    # dev-build dycore
    if cosmo_spec.satisfies('+cppdycore'):
        args.spec = dycore_spec
        dev_build(self, args)
        args.spec = str(cosmo_spec) + ' ^' + dycore_spec

     # dev-build cosmo
    dev_build(self, args)
