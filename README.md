# Boids Utils

Interacts with the k8s cluster based on Boids events

## Development Environment

### Prerequisites:

TBP

### Running inside the container

```
$ export PYTHONPATH=/opt/boids-k8s-events/src:/usr/local/lib/python3.11/site-packages:${PYTHONPATH}
# ./boids-k8s-events.py -v /etc/boids/logging.yaml /etc/boids/pubsub.yaml
```

### Running Unit Tests

**NOTE:** A valid kubectl config file must exist at ~python/.kube/config

```
$ export PYTHONPATH=/opt/boids-k8s-events/src:/usr/local/lib/python3.11/site-packages:${PYTHONPATH}

$ pytest test

$ pylint src
```
