init:
	terraform init \
	./terraform

build:
	terraform apply \
	-var-file="terraform/config/config.tfvars" \
	-var-file="terraform/config/config.tfvars.secret" \
	./terraform

plan:
	terraform plan \
	-var-file="terraform/config/config.tfvars" \
	-var-file="terraform/config/config.tfvars.secret" \
	./terraform

destroy:
	terraform destroy \
	-var-file="terraform/config/config.tfvars" \
	-var-file="terraform/config/config.tfvars.secret" \
	./terraform
