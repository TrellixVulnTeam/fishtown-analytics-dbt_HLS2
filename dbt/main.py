import argparse
import os.path
import sys
import dbt.project as project
import dbt.task.run as run_task
import dbt.task.compile as compile_task
import dbt.task.debug as debug_task
import dbt.task.clean as clean_task
import dbt.task.deps as deps_task


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if os.path.isfile('dbt_project.yml'):
        proj = project.read_project('dbt_project.yml')
    else:
        raise RuntimeError("dbt must be run from a project root directory with a dbt_project.yml file")

    p = argparse.ArgumentParser(prog='dbt: data build tool')
    subs = p.add_subparsers()

    sub = subs.add_parser('clean')
    sub.set_defaults(cls=clean_task.CleanTask)

    sub = subs.add_parser('compile')
    sub.set_defaults(cls=compile_task.CompileTask)

    sub = subs.add_parser('debug')
    sub.set_defaults(cls=debug_task.DebugTask)

    sub = subs.add_parser('deps')
    sub.set_defaults(cls=deps_task.DepsTask)

    sub = subs.add_parser('run')
    sub.set_defaults(cls=run_task.RunTask)

    parsed = p.parse_args(args)

    parsed.cls(args=parsed, project=proj).run()