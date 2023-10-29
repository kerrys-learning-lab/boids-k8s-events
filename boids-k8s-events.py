#! /usr/bin/env python3
""" Interacts with the k8s cluster based on Boids events """
import argparse
import asyncio
import logging
import boids.k8s_events
import boids_utils.config
import boids_utils.logging
import boids_utils.openapi
import boids_utils.pubsub
import boids_utils.template

LOGGER = logging.getLogger('boids-k8s-events')


# Order is important
# - utils.config *must* be first in order to load all configuration files
#   for subsequent stakeholders
# - utils.logging *should* be early in order to facilitate debugging
CLI_STAKEHOLDERS = [
    boids_utils.config,
    boids_utils.logging,
    boids_utils.openapi,
    boids_utils.pubsub,
    boids_utils.template
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Boids K8s events')

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.add_cli_options(parser)

    args = parser.parse_args()

    for stakeholder in CLI_STAKEHOLDERS:
        stakeholder.process_cli_options(args, **boids_utils.config.instance)

    callback = boids.k8s_events.SessionConfigurationStatusConsumer()
    boids_utils.pubsub.add_topic_callback('boids.sessions', callback)

    asyncio.get_event_loop().run_forever()
