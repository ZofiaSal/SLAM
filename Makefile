init:
	pip3 install -r requirements.txt

test:
	bash ./synthetic_tests/running_tests.sh

clean:
	rm -rf __pycache__