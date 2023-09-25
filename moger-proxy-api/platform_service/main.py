from fastapi import FastAPI
from mangum import Mangum
import logging
import boto3
from botocore.config import Config

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_eks_node_groups():
    my_config = Config(region_name = 'us-west-2')
    client = boto3.client("eks", config=my_config)
    response = client.list_clusters(
        maxResults=23,
    )    
    cluster_name = response['clusters'][0]
    logger.info(f"our cluster is {cluster_name}")

    response = client.list_nodegroups(clusterName=cluster_name, maxResults=23)

    logger.info(f"here is our node groups {response['nodegroups']}")

    node_groups = response['nodegroups']
    return cluster_name, node_groups

def get_eks_cluster():
    my_config = Config(region_name = 'us-west-2')
    client = boto3.client("eks", config=my_config)
    response = client.list_clusters(
        maxResults=23,
    )    
    cluster_name = response['clusters'][0]
    logger.info(f"our cluster is {cluster_name}")

    response = client.list_nodegroups(clusterName=cluster_name, maxResults=23)

    logger.info(f"here is our node groups {response['nodegroups']}")

    node_groups = response['nodegroups']
    nodegroup_sizes = {}
    nodegroup_minsizes = {}
    nodegroup_maxsizes = {}
    for node in node_groups:
        response = client.describe_nodegroup(clusterName=cluster_name, nodegroupName=node)
        scaling_config = response['nodegroup']['scalingConfig']
        # logger.info(f"here is the scaling config {scaling_config} for node {node}")
        nodegroup_sizes[node] = scaling_config['desiredSize']
        nodegroup_maxsizes[node] = scaling_config['maxSize']
        nodegroup_minsizes[node] = scaling_config['maxSize']

    logger.info(f"here is the nodegroup_sizes {nodegroup_sizes}")
    logger.info(f"here is the nodegroup_maxsizes {nodegroup_maxsizes}")
    logger.info(f"here is the nodegroup_minsizes {nodegroup_minsizes}")

    return nodegroup_sizes, nodegroup_minsizes, nodegroup_maxsizes

@app.get("/")
async def greeting_world():

    get_eks_cluster()

    return {"message": "hello world"}

handler = Mangum(app)

