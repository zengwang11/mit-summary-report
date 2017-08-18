# coding: utf-8
import json
import watson_developer_cloud

discovery = watson_developer_cloud.DiscoveryV1(
    '2016-11-07',
    username="a1582e86-98b0-4041-8fac-9c01aa85f964",
    password="kiDEgM7oCRW7")

environments = discovery.get_environments()
#print(json.dumps(environments, indent=2))

news_environments = [x for x in environments['environments'] if
                      x['name'] == "my-first-environment"]
news_environment_id = news_environments[0]['environment_id']
#print(json.dumps(news_environment_id, indent=2))

collections = discovery.list_collections(news_environment_id)
news_collections = [x for x in collections['collections']]
#print(json.dumps(collections, indent=2))

configurations = discovery.list_configurations(
    environment_id=news_environment_id)
#print(json.dumps(configurations, indent=2))
default_config_id = discovery.get_default_configuration_id(
    environment_id=news_environment_id)
#print(json.dumps(default_config_id, indent=2))

default_config = discovery.get_configuration(
    environment_id=news_environment_id, configuration_id=default_config_id)
#print(json.dumps(default_config, indent=2))

keyword = raw_input("Please type in the key word:")
query_options = {'query': keyword}
query_results = discovery.query(news_environment_id,
                                news_collections[0]['collection_id'],
                                query_options)
print(json.dumps(query_results, indent=2))
