from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import logging
import boto3
import os
from botocore.config import Config

app = FastAPI()


origins = os.environ["ALLOWED_CROSS_ORIGIN"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
my_config = Config(region_name = 'us-west-2')
eks = boto3.client("eks", config=my_config)

def get_eks_node_groups():
    response = eks.list_clusters(
        maxResults=23,
    )    
    cluster_name = response['clusters'][0]
    logger.info(f"our cluster is {cluster_name}")

    response = eks.list_nodegroups(clusterName=cluster_name, maxResults=23)

    logger.info(f"here is our node groups {response['nodegroups']}")

    node_groups = response['nodegroups']
    return cluster_name, node_groups

def get_eks_cluster():
    response = eks.list_clusters(
        maxResults=23,
    )    
    cluster_name = response['clusters'][0]
    logger.info(f"our cluster is {cluster_name}")

    response = eks.list_nodegroups(clusterName=cluster_name, maxResults=23)

    logger.info(f"here is our node groups {response['nodegroups']}")

    node_groups = response['nodegroups']
    nodegroup_sizes = {}
    nodegroup_minsizes = {}
    nodegroup_maxsizes = {}
    for node in node_groups:
        response = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=node)
        scaling_config = response['nodegroup']['scalingConfig']
        # logger.info(f"here is the scaling config {scaling_config} for node {node}")
        nodegroup_sizes[node] = scaling_config['desiredSize']
        nodegroup_maxsizes[node] = scaling_config['maxSize']
        nodegroup_minsizes[node] = scaling_config['maxSize']

    logger.info(f"here is the nodegroup_sizes {nodegroup_sizes}")
    logger.info(f"here is the nodegroup_maxsizes {nodegroup_maxsizes}")
    logger.info(f"here is the nodegroup_minsizes {nodegroup_minsizes}")

    return cluster_name, nodegroup_sizes, nodegroup_minsizes, nodegroup_maxsizes

@app.get("/")
async def greeting_world():

    get_eks_cluster()

    return {"message": "hello world"}

@app.post("/eks/scale-up")
async def scale_up_eks_cluster():
    cluster_name, nodegroup_sizes, nodegroup_minsizes, nodegroup_maxsizes = get_eks_cluster()

    for nodegroup_name, max_size in nodegroup_maxsizes.items():
        response = eks.describe_nodegroup(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name
        )
        current_size = response['nodegroup']['scalingConfig']['maxSize']

        if max_size != current_size:
            response = eks.update_nodegroup_config(
                clusterName=cluster_name,
                nodegroupName=nodegroup_name,
                scalingConfig={
                    'maxSize': max_size
                }
            )
            print(
                f"Updated maximum size for node group {nodegroup_name} to {max_size}")
        else:
            print(
                f"Maximum size is already {max_size} for node group {nodegroup_name}")

    for nodegroup_name, desired_size in nodegroup_sizes.items():
        response = eks.describe_nodegroup(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name
        )
        current_size = response['nodegroup']['scalingConfig']['desiredSize']

        if desired_size != current_size:
            response = eks.update_nodegroup_config(
                clusterName=cluster_name,
                nodegroupName=nodegroup_name,
                scalingConfig={
                    'desiredSize': desired_size
                }
            )
            print(
                f"Updated desired size for node group {nodegroup_name} to {desired_size}")
        else:
            print(
                f"Desired size is already {desired_size} for node group {nodegroup_name}")

    for nodegroup_name, min_size in nodegroup_minsizes.items():
        response = eks.describe_nodegroup(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name
        )
        current_size = response['nodegroup']['scalingConfig']['minSize']

        if min_size != current_size:
            response = eks.update_nodegroup_config(
                clusterName=cluster_name,
                nodegroupName=nodegroup_name,
                scalingConfig={
                    'minSize': min_size
                }
            )
            print(
                f"Updated minimal size for node group {nodegroup_name} to {min_size}")
        else:
            print(
                f"Minimal size is already {min_size} for node group {nodegroup_name}")
    return JSONResponse(status_code=200, content={"message": "scaling up eks cluster"})

@app.post("/eks/scale-down")
async def scale_down_eks_cluster():
    cluster_name, nodegroup_names = get_eks_node_groups()
    
    new_desiredSize = 0
    new_minSize = 0
    new_maxSize = 1

    # Loop through the node groups and update their desired capacity to 0
    for nodegroup_name in nodegroup_names:
        response = eks.update_nodegroup_config(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
            scalingConfig={
                "desiredSize": new_desiredSize,
                "minSize": new_minSize,
                "maxSize": new_maxSize
            }
        )

        # Print the response
        logger.info(response)

    return JSONResponse(status_code=200, content={"message": "scaling down eks cluster"})


@app.get("/healthcheck")
def perform_healthcheck():
    region = os.environ["AWS_REGION_NAME"]
    request_info = {
        "message": "Moger Platform API: Called HealthCheck",
        "region": region,
    }
    logger.info(request_info)

    return {"healthcheck": "Everything OK!", "region": region}

handler = Mangum(app)

