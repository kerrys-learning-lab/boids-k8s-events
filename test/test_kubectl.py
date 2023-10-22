import argparse
import logging
import boids.k8s_events.kubectl

LOGGER = logging.getLogger(__name__)

def test_get_resource_deployments(test_cli_args: argparse.Namespace):
    deployments = boids.k8s_events.kubectl.get_resource('deployments')

    assert len(deployments) > 0

    for dep in deployments:
        LOGGER.debug(dep['metadata']['labels']['app.kubernetes.io/name'])
