
# TOP Level file structure of ansible framework

my_ansible_project/
├── ansible.cfg          # Ansible configuration file
├── inventory/           # Directory for inventory files and scripts
│   ├── hosts              # Static inventory file
│   ├── group_vars/        # Directory for group-specific variables
│   │   ├── webservers.yml
│   │   └── dbservers.yml
│   └── host_vars/         # Directory for host-specific variables
│       ├── server1.yml
│       └── server2.yml
├── playbooks/           # Directory for your Ansible playbooks
│   ├── web_deploy.yml
│   ├── db_setup.yml
│   └── update_all.yml
├── roles/               # Directory for Ansible roles (highly recommended for organization)
│   ├── webserver/
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── files/
│   │   │   └── nginx.conf
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── meta/
│   │   │   └── main.yml
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── index.html.j2
│   │   └── vars/
│   │       └── main.yml
│   └── database/
│       └── ...
└── library/             # Optional: Custom Ansible modules


# provides Organization, Reusability, Maintability, Collaboration

__ansible.cfg:__ This is the main configuration file for Ansible. You can set various parameters here, such as the default inventory location, remote user, connection settings, and more. It's often placed at the root of your project but can also exist in other locations.

__inventory/:__ This directory houses your inventory files, which define the hosts and groups of hosts that Ansible will manage.

__hosts:__ A common name for a static inventory file. It lists your managed nodes, their IP addresses or hostnames, and any group assignments or host-specific variables. You can have multiple inventory files.

__group_vars/:__ This directory contains YAML files that define variables applicable to specific groups defined in your inventory. The filename should match the group name (e.g., webservers.yml for the webservers group).

__host_vars/:__ Similar to group_vars/, this directory holds YAML files containing variables specific to individual hosts. The filename should match the hostname as defined in your inventory (e.g., server1.yml for the host named server1).

__playbooks/:__ This directory is where you'll store your Ansible playbooks. Playbooks are YAML files that define the automation tasks to be executed on your managed hosts. They orchestrate the configuration and management of your systems.

__roles/:__ This is a crucial directory for organizing your Ansible content. Roles allow you to encapsulate tasks, handlers, variables, templates, and other Ansible components into reusable units. A typical role directory structure looks like the webserver/ example above:

__defaults/main.yml:__ Contains default variables for the role. These have the lowest precedence and can be overridden.
__files/:__ Stores static files that can be copied to managed hosts using the copy module.
__handlers/main.yml:__ Contains handlers, which are special tasks that are only run when explicitly notified by other tasks.

__meta/main.yml:__ Defines metadata about the role, such as its author, license, and dependencies.

__tasks/main.yml:__ The primary file containing the main sequence of tasks to be executed by the role. You can also break down tasks into multiple files within this directory and include them in main.yml.

__templates/:__ Stores Jinja2 template files that can be dynamically rendered and copied to managed hosts using the template module.

__vars/main.yml:__ Contains variables specific to the role. These have a higher precedence than default variables.

__library/:__ This is an optional directory where you can store custom Ansible modules that you've developed. Ansible has a vast library of built-in modules, but you might create your own for specific needs.
