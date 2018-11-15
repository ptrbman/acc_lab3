create-stack:
	openstack stack create -t stack.yaml ptr-stack

create-min-stack:
	openstack stack create -t stack.yaml --parameter slave_count=0 ptr-stack

create-full-stack:
	openstack stack create -t stack.yaml --parameter slave_count=10 ptr-stack

worker-0:
	openstack stack update -t stack.yaml --parameter slave_count=0 ptr-stack

worker-1:
	openstack stack update -t stack.yaml --parameter slave_count=1 ptr-stack

worker-2:
	openstack stack update -t stack.yaml --parameter slave_count=2 ptr-stack

worker-3:
	openstack stack update -t stack.yaml --parameter slave_count=3 ptr-stack

worker-4:
	openstack stack update -t stack.yaml --parameter slave_count=4 ptr-stack

worker-5:
	openstack stack update -t stack.yaml --parameter slave_count=5 ptr-stack

worker-6:
	openstack stack update -t stack.yaml --parameter slave_count=6 ptr-stack

worker-7:
	openstack stack update -t stack.yaml --parameter slave_count=7 ptr-stack

worker-8:
	openstack stack update -t stack.yaml --parameter slave_count=8 ptr-stack

worker-9:
	openstack stack update -t stack.yaml --parameter slave_count=9 ptr-stack

worker-10:
	openstack stack update -t stack.yaml --parameter slave_count=10 ptr-stack

update-stack:
	openstack stack update -t stack.yaml ptr-stack

show-stack:
	openstack stack show --fit-width ptr-stack

delete-stack:
	openstack stack delete ptr-stack
