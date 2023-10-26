import asyncio
import logging
import os.path
import uuid
import pytest
import boidsapi.model
import boids.k8s_events.kubectl
import boids_utils
import boids_utils.pubsub

LOGGER = logging.getLogger(__name__)

def create_test_session_config(count=1, title='Test title', num_boids=10):
    results = []
    for i in range(count):
        value = boidsapi.model.SessionConfigurationStatus(title=f'{title} {i}',
                                                          num_boids=num_boids,
                                                          state= boidsapi.model.SessionState.PENDING,
                                                          uuid=boids_utils.mk_uuid(),
                                                          created=boids_utils.nowutc(stringify=True),
                                                          modified=boids_utils.nowutc(stringify=True))
        results.append(value)
    return results if count > 1 else results[0]

@pytest.mark.asyncio
@pytest.mark.timeout(60)
async def test_session_pending():
    consumer = boids.k8s_events.SessionConfigurationStatusConsumer()

    session: boidsapi.model.SessionConfigurationStatus = create_test_session_config()

    message = boids_utils.pubsub.Message(topic='boids.sessions', value=session.to_dict())

    consumer.on_message(message)

    found_deployment = False
    while not found_deployment:
        deployments = boids.k8s_events.kubectl.get_resource('deployments')

        for dep in deployments:
            if dep['metadata'].get('name') == f'engine-{session.uuid}-deployment':
                found_deployment = True
                break

        if not found_deployment:
            await asyncio.sleep(1)

    session.state = boidsapi.model.SessionState.ARCHIVED

    message = boids_utils.pubsub.Message(topic='boids.sessions', value=session.to_dict())

    consumer.on_message(message)
    while found_deployment:
        found_deployment = False
        deployments = boids.k8s_events.kubectl.get_resource('deployments')

        for dep in deployments:
            if dep['metadata'].get('name') == f'engine-{session.uuid}-deployment':
                found_deployment = True
                break

        if found_deployment:
            await asyncio.sleep(1)
