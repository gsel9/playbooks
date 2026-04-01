# 1. Create index
# 2. Upload docs 
# 3. Create knowledge source
# 4. Create knowledge base

import config


def main():

    config.load_config()

    search_endpoint = config.require_env(config.AZURE_SEARCH_ENDPOINT)
    index_name = config.require_env(config.AZURE_SEARCH_INDEX)


if __name__ == "__main__":
    main()
