create-stack:
	openstack stack create -t stack.yaml ptr-stack

show-stack:
	openstack stack show --fit-width ptr-stack

delete-stack:
	openstack stack delete ptr-stack
