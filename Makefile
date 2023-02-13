



COMMUNE=commune
SUBSPACE=subspace
SUBTENSOR=194.163.191.101:9944
PYTHON=python3




down:
	./$(COMMUNE).sh --all --down

stop:
	make down
up:
	./$(COMMUNE).sh --all
start:
	./$(COMMUNE).sh --${arg} 
logs:
	./$(COMMUNE).sh --${arg}

build:
	./$(COMMUNE).sh --build --${arg}

subspace:
	make bash arg=$(SUBSPACE)

enter: 
	make bash arg=$(COMMUNE)
restart:
	./$(COMMUNE).sh --${arg} --restart

prune_volumes:	
	docker system prune --all --volumes

bash:
	docker exec -it ${arg} bash

app:
	make streamlit


kill_all:
	docker kill $(docker ps -q)

logs:
	docker logs ${arg} --tail=100 --follow

streamlit:
	docker exec -it commune bash -c "streamlit run $(COMMUNE)/${arg}.py "
	
enter_backend:
	docker exec -it backend bash

pull:
	git submodule update --init --recursive
	
kill_all_containers:
	docker kill $(docker ps -q) 

python:
	docker exec -it backend bash -c "python ${arg}.py"

exec:

	docker exec -it backend bash -c "${arg}"

build_protos:
	python -m grpc_tools.protoc --proto_path=${PWD}/$(COMMUNE)/proto ${PWD}/$(COMMUNE)/proto/commune.proto --python_out=${PWD}/$(COMMUNE)/proto --grpc_python_out=${PWD}/$(COMMUNE)/proto


api:  
	uvicorn $(COMMUNE).api.api:app --reload

ray_start:
	ray start --head --port=6379 --redis-port=6379 --object-manager-port=8076 --node-manager-port=8077 --num-cpus=4 --num-gpus=0 --memory=1000000000 --object-store-memory=1000000000

ray_stop:
	ray stop

ray_status:
	ray status

miner:
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python pm2 start commune/model/client/model.py --name miner_${coldkey}_${hotkey} --time --interpreter $(PYTHON) --  --logging.debug  --subtensor.chain_endpoint 194.163.191.101:9944 --wallet.name ${coldkey} --wallet.hotkey ${hotkey} --axon.port ${port} 

vali:
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python pm2 start commune/block/bittensor/neuron/validator/neuron.py --name vali_${coldkey}_${hotkey} --time --interpreter python3 -- --logging.debug --subtensor.network local  --neuron.device cuda:1 --wallet.name ${coldkey} --wallet.hotkey ${hotkey} --logging.trace True --logging.record_log True  --neuron.print_neuron_stats True

dashboard:
	streamlit run commune/block/bittensor/dashboard.py 