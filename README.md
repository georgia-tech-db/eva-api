# DB API for EVA

## Install

Installation of EVA involves setting a virtual environment using miniconda.

Clone the repository
```shell
git clone https://github.com/georgia-tech-db/eva-api.git
```
Go into the demo branch.

Install the dependencies.
```shell
sh script/install/before_install.sh
export PATH="$HOME/miniconda/bin:$PATH"
sh script/install/install.sh
```
# Local changes
Copy all files in demo folder to outside the demo folder.

In config.py, change line 4 to FLASK_HOST = “0.0.0.0” and line 5 to FLASK_PORT=5000. Change line 8 to EVA_HOST= [the host address that eva.py is running on, likely “0.0.0.0”] and line 9 to EVA_PORT= [the port eva.py is running on].

In demo_api.py, look at the get_frames function. Change the hostname and port variables to the ones used for EVA_HOST and EVA_PORT in config.py. 


# Running EVA-API
First, start running EVA in a separate terminal. Then, run:

```shell
conda activate eva_api
python run_before_startup.py  # Only run after EVA has started running
python demo_api.py
```
For the first time you run this, errors may pop up about not having libraries installed. Simply use pip install [package] to install each package it asks for.

Default host and port for EVA server is 0.0.0.0:5432

## DB API
Currently supported APIs:
- connect / connect_async
- cursor
- execute / execute_async
- fetch_one / fetch_one_async
- fetch_all / fetch_all_async

Usage: check [db_api_example.py](db_api_example.py)

**Notice: Both asyncio and sync APIs have been provided. However sync APIs are auto-generated from asyncio APIs,
so avoiding using sync APIs in an environment that contains asyncio.**

## Contributing

To file a bug or request a feature, please file a GitHub issue. Pull requests are welcome.

## Contributors

See the [people page](https://github.com/georgia-tech-db/eva/graphs/contributors) for the full listing of contributors.

## License
Copyright (c) 2018-2020 [Georgia Tech Database Group](http://db.cc.gatech.edu/)
Licensed under the [Apache License](LICENSE).
