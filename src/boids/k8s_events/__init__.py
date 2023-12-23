""" Responds to SessionConfigurationStatus messages """
import logging
import os
import traceback
import jinja2.exceptions
import boids_api.boids
import boids_utils.pubsub
import boids_utils.template
import boids.k8s_events.kubectl

LOGGER = logging.getLogger(__name__)

class SessionConfigurationStatusConsumer(boids_utils.pubsub.ConsumerCallback):
    """ Responds to SessionConfigurationStatus messages """

    def on_message(self, message: boids_utils.pubsub.Message):
        try:
            LOGGER.debug(f'SessionConfigurationStatusConsumer.on_message(message={message.value.get("title", "<no-title>")})')
            session_status = boids_api.boids.SessionConfigurationStatus.from_dict(message.value)

            if session_status.state == boids_api.boids.SessionState.PENDING:
                LOGGER.info(f'Instantiating boids-engine for session {session_status.uuid}')
                k8s_template_context = SessionConfigurationStatusConsumer._create_k8s_template(session_status)

                with k8s_template_context as _:
                    boids.k8s_events.kubectl.apply(k8s_template_context.path)

            elif session_status.state == boids_api.boids.SessionState.ARCHIVED:
                LOGGER.info(f'Terminating boids-engine for session {session_status.uuid}')
                k8s_template_context = SessionConfigurationStatusConsumer._create_k8s_template(session_status)

                with k8s_template_context as _:
                    boids.k8s_events.kubectl.delete(k8s_template_context.path)
        except jinja2.exceptions.TemplateError as ex:
            LOGGER.error(f'{type(ex).__name__}: {ex.message}')

    @staticmethod
    def _create_k8s_template(session_status: boids_api.boids.SessionConfigurationStatus):
        # TODO: Get Pod labels to pass in to template # pylint: disable=fixme
        return boids_utils.template.render('boids-engine-k8s.yaml.j2',
                                        uuid=session_status.uuid,
                                        image_spec=os.environ.get('BOIDS_ENGINE_IMAGE_SPEC',
                                                                    'boids-engine:latest'),
                                        labels={},
                                        annotations={})
