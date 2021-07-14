# ConfigLoader

The ConfigLoader package is a Python package that can be used to load application specific configuration, like database settings. It can be used in conjunction with environment variables and it can use different environments, like `production`, `acceptation` and `development`.

## Usage

The package contains a static ConfigLoader class that should be used to load configuration. The way to use it, is to first use the `load_settings` static method on the class. That returns a boolean to indicate if the loading was successfull. If it was, you can get the configuration by using the `config` dict on the class.

The configurationfile that it tries to load, is a file with the name `config.yaml` and should be in YAML format. You can change this by calling the `set_file` method before retrieving the config, or by specifing the file in a environment variable `CONFIG_FILE`. You can also specify the file with the `yaml_file` parameter of the `load_settings` method.

You can set a environment to use with the environment variable `ENVIORNMENT` or by using the `set_environment` method.

The configuration YAML file should be in the following format:

```yaml
---
default:
  environments:
    - "production"
    - "development"
  config:
    logging:
      level: 40
    database:
      type: "mysql"
      server: "${env:DB_SERVER}"
      username: "${env:DB_USERNAME}"
      password: "${env:DB_PASSWORD}"
      database: "${env:DB_DATABASE}"
    sql_alchemy:
      echo: False
      pool_pre_ping: true
      pool_recycle: 10
      pool_size: 5
      pool_overflow: 10
      create_tables: false

development:
  sql_alchemy:
    pool_echo: true
    create_table: true
  logging:
    level: 10
```

The `default` key specifies default values for the application. It specifies possible environments and a default `config`. In other root elements, you can override the defaults for specific environments. In the example above, the `pool_echo` variable gets set to a default value of `false`, but will be overwritten for the development environment.

### Example

Using the example configuration file above, we can use the following Python code to create a connection to the database:

```python
from config_loader import ConfigLoader

# Load the settings
if not ConfigLoader.load_settings():
    raise Exception(f'Configuration was not yet loaded.')

# Connect to the database
database.connect(
    username = ConfigLoader.config['database']['username'],
    password = ConfigLoader.config['database']['password'],
    server = ConfigLoader.config['database']['server'],
    database = ConfigLoader.config['database']['database'],
)
```