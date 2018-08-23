IMAGE_PREFIX=index.alauda.cn/alaudaorg
IMAGE=cat-prediction-web
TAG=latest

YAML_NS=aml
YAML_NAME=z

build-image:
	docker build -t  ${IMAGE_PREFIX}/${IMAGE}:${TAG}  -f docker/Dockerfile .

yaml:
	helm template --name ${YAML_NAME} --namespace ${YAML_NS} deploy/cat-prediction-web > cat-prediction-web.yaml
