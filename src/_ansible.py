from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.plugins.loader import init_plugin_loader
import yaml, os


def renderTemplate(yamlVars, jinjaTemplate):
    # Create a callback plugin so we can capture the output
    class ResultsCollectorJSONCallback(CallbackBase):
        def __init__(self, *args, **kwargs):
            super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
            self.host_ok = {}
            self.host_unreachable = {}
            self.host_failed = {}

        def v2_runner_on_unreachable(self, result):
            host = result._host
            self.host_unreachable[host.get_name()] = result

        def v2_runner_on_ok(self, result, *args, **kwargs):
            host = result._host
            self.host_ok[host.get_name()] = result

        def v2_runner_on_failed(self, result, *args, **kwargs):
            host = result._host
            self.host_failed[host.get_name()] = result

    init_plugin_loader()
    loader = DataLoader()

    context.CLIARGS = ImmutableDict(
        tags={},
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        connection="ssh",
        module_path=None,
        forks=100,
        remote_user="xxx",
        private_key_file=None,
        ssh_common_args=None,
        ssh_extra_args=None,
        sftp_extra_args=None,
        scp_extra_args=None,
        become=True,
        become_method="sudo",
        become_user="root",
        verbosity=True,
        check=False,
        start_at_task=None,
    )

    results_callback = ResultsCollectorJSONCallback()

    inventory = InventoryManager(loader=loader)
    inventory.add_host("localhost", group="all")
    host = inventory.get_host("localhost")
    host.vars.update(yaml.load(yamlVars, Loader=yaml.FullLoader))

    inventory.reconcile_inventory()

    variable_manager = VariableManager(
        loader=loader, inventory=inventory, version_info=CLI.version_info(gitinfo=False)
    )

    with open("template.j2", "w") as file:
        file.write(rf"{jinjaTemplate}")
        file.close()

    play_source = dict(
        name="Ansible Play",
        hosts="localhost",
        gather_facts="no",
        tasks=[
            dict(
                action=dict(
                    module="ansible.builtin.set_fact",
                    args='output={{ lookup("template", "template.j2" ) }}',
                ),
                register="shell_out",
            ),
        ],
    )

    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=dict(vault_pass=""),
        stdout_callback=results_callback,
    )

    tqm.run(play)
    os.remove("template.j2")
    if len(results_callback.host_failed) > 0:
        print("ERROR")
        output = results_callback.host_failed["localhost"]._result["msg"]
        return (output, True)
    else:
        if len(results_callback.host_ok) > 0:
            output = results_callback.host_ok["localhost"]._result["ansible_facts"][
                "output"
            ]
            return (output, False)
