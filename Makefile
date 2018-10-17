lint-mypy:
	mypy pandora

test:
	ci/run_test.sh

doc:
	pipenv run python manage.py openapi-doc > /mfs/swagger/docs/pandora.json
	echo "Doc is avaliable at https://swagger-d2.xiachufang.com/?url=https://swagger-d2.xiachufang.com/docs/pandora.json"
