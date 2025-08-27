# This script manages ECS instances on Open Telekom Cloud (OTC).
# ECS API Value	Meaning
# ACTIVE	Running
# SHUTOFF	Stopped
# BUILD	Creating
# STOPPING	Stopping (transitional)
# STARTING	Starting (transitional)
# ERROR	Error state

import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkecs.v2 import *
import time

def get_ecs_client():
    """
    Initializes and returns an ECS client for Open Telekom Cloud.
    """
    ak = os.environ.get("OTC_access_key_id")
    sk = os.environ.get("OTC_secret_access_key")
    project_id = os.environ.get("OTC_project_id")

    if not ak or not sk or not project_id:
        print("Error: OTC_access_key_id, OTC_secret_access_key, or OTC_project_id environment variables are not set.")
        print("Please set them before running the script.")
        exit(1)

    # Initialize credentials with Access Key, Secret Key, and Project ID
    credentials = BasicCredentials(ak, sk, project_id)

    # Initialize the ECS client with credentials and region
    client = EcsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(Region(id="eu-de", endpoint="https://ecs.eu-de.otc.t-systems.com")) \
        .build()
    return client

def start_ecs_instances_otc(client, instance_ids):
    """
    Starting ECS instances.
    """
    servers = [{"id": instance_id} for instance_id in instance_ids]
    option = BatchStartServersOption(servers=servers)
    request_body = BatchStartServersRequestBody(os_start=option)
    request = BatchStartServersRequest(body=request_body)

    try:
        response = client.batch_start_servers(request)
        print("   Start response:", response)
    except Exception as e:
        print("   Error starting instances:", e)



def stop_ecs_instances_otc(client, instance_ids):
    """
    Stopping ECS instances.
    """
    servers = [{"id": instance_id} for instance_id in instance_ids]
    option = BatchStopServersOption(servers=servers, type="SOFT")  # type can be "SOFT" or "HARD"
    request_body = BatchStopServersRequestBody(os_stop=option)
    request = BatchStopServersRequest(body=request_body)

    try:
        response = client.batch_stop_servers(request)
        print("   Stop response:", response)
    except Exception as e:
        print("   Error stopping instances:", e)

def get_ecs_instance_status(client, instance_id):
    """
    Getting ECS instance status.
    """
    try:
        request = ShowServerRequest(server_id=instance_id)
        response = client.show_server(request)
        status = response.server.status  # e.g., "ACTIVE", "SHUTOFF"
        print(f"      Instance {instance_id} status: {status}")
        return status
    except Exception as e:
        print(f"      Error retrieving instance status: {e}")
        return None

def wait_for_status(client, instance_id, target_status, timeout=300, interval=10):
    """
    Waiting for ECS status.
    """
    elapsed = 0
    while elapsed < timeout:
        status = get_ecs_instance_status(client, instance_id)
        if status == target_status:
            print(f"     Instance {instance_id} reached target status: {target_status}")
            return True
        print(f"     Waiting for instance {instance_id} to reach status: {target_status} (current: {status})")
        time.sleep(interval)
        elapsed += interval
    print(f"     Timeout waiting for instance {instance_id} to reach status: {target_status}")
    return False


if __name__ == "__main__":
    """
    Main script to manage ECS instances on Open Telekom Cloud.
    """
    Frontend_INSTANCE_IDS = ['5d5b0d7f-bdd0-48c4-8bf7-f7f5a86b1cf1', '1840028a-5e62-44c6-85df-a19f8f18e21e'] # Your Frontend ECS Instance IDs
    Backend_INSTANCE_IDS = ['d16a87a1-3f47-4eac-b6ee-54bff5e6006b', 'bca1530e-7b13-4afb-9da1-e23ac4d36d8b'] # Your Backend ECS Instance IDs
    client = get_ecs_client() # Initialize the ECS client
    print("Choose an action: 'start' or 'stop'.")
    action = input("Enter action (start/stop): ").strip().lower()
    if action == 'start':
        print("Starting Backend servers.")
        start_ecs_instances_otc(client, Backend_INSTANCE_IDS)
        all_started = all(wait_for_status(client, instance_id, "ACTIVE") for instance_id in Backend_INSTANCE_IDS)
        if all_started:
            print("All Backend servers started successfully.")
            print("Starting Frontend servers.")
            start_ecs_instances_otc(client, Frontend_INSTANCE_IDS)
            all_started = all(wait_for_status(client, instance_id, "ACTIVE") for instance_id in Frontend_INSTANCE_IDS)
            if all_started:
                print("All Frontend servers started successfully.")
            else:
                print("Some Frontend servers failed to start.")    
        else:
            print("Some Backend servers failed to start.")
    elif action == 'stop':
        print("Stopping Frontend servers.")
        stop_ecs_instances_otc(client, Frontend_INSTANCE_IDS)
        all_stopped = all(wait_for_status(client, instance_id, "SHUTOFF") for instance_id in Frontend_INSTANCE_IDS)
        if all_stopped:
            print("All Frontend servers stopped successfully.")
            print("Stopping Backend servers.")
            stop_ecs_instances_otc(client, Backend_INSTANCE_IDS)
            all_stopped = all(wait_for_status(client, instance_id, "SHUTOFF") for instance_id in Backend_INSTANCE_IDS)
            if all_stopped:
                print("All Backend servers stopped successfully.")
            else:
                print("Some Backend servers failed to stop.")
        else:
            print("Some Frontend servers failed to stop.")
    else:
        print("Invalid action. Please enter 'start' or 'stop'.")

    