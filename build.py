from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "micro-utilities"
default_task = "publish"


@init
def set_properties(project):
    build_number = project.get_property("build_number")
    if build_number is not None and "" != build_number:
        project.version = build_number
    else:
        project.version = "0.0.999"
    project.depends_on_requirements("src/main/python/requirements.txt")
    project.set_property('unittest_module_glob', 'test_*')
    project.set_property('coverage_branch_threshold_warn', 40)
    project.set_property('coverage_branch_partial_threshold_warn', 40)
