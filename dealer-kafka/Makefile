all:
	$(error Please pick a target (use `make list` to view them))


list:
	@egrep '^[^[:space:]]+:' Makefile | grep -v .PHONY | tr -d :

run-processor:
	2>&1 ./run_processor.py -c 2 | tee processor.log

sync:
	@rsync \
	    -e ssh \
	    -avz . yaron:dealer-kafka

#	    -avz . 34.230.69.143:dealer-kafka


.PHONY: list all sync run-processor
