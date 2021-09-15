run from bb_api/templates

docker run --rm --name slate -v $(pwd)/api_docs_source/config.rb:/srv/slate/config.rb -v $(pwd)/api_docs_source/build:/srv/slate/build -v $(pwd)/api_docs_source:/srv/slate/source slatedocs/slate
