# DB API for EVA

## Install

Installation of EVA involves setting a virtual environment using miniconda.

1. Clone the repository
```shell
git clone https://github.com/georgia-tech-db/eva-api.git
```

2. Install the dependencies.
```shell
sh script/install/before_install.sh
export PATH="$HOME/miniconda/bin:$PATH"
sh script/install/install.sh
```

## Command Line Client

```shell
conda activate eva_api
python eva_cmd_client.py -H [host] -P [port]
```
Default host and port for EVA server is 0.0.0.0:5432

## DB API
Currently supported APIs:
- connect / connect_async
- cursor
- execute / execute_async
- fetch_one / fetch_one_async
- fetch_all / fetch_all_async

Usage: check [db_api_example.py](dp_api_example.py)

**Notice: Both asyncio and sync APIs have been provided. However sync APIs are auto-generated from asyncio APIs,
so avoiding using sync APIs in an environment that contains asyncio.**

## Contributing

To file a bug or request a feature, please file a GitHub issue. Pull requests are welcome.

## Contributors

See the [people page](https://github.com/georgia-tech-db/eva/graphs/contributors) for the full listing of contributors.

## License
Copyright (c) 2018-2020 [Georgia Tech Database Group](http://db.cc.gatech.edu/)
Licensed under the [Apache License](LICENSE).
