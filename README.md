# kguru

kguru (:KeiGuRu:) is an agnostic, declarative and distributed Infrastructure as Code (IaC) manager.

It is inspired by IaC projects like kubernetes, crossplane, terraform, etc. In fact, *kguru* stands for "kubernetes-guru" even though it is much more abstract and high-level than k8s.


## Design concepts

Each action is a boolean functions that takes params as payload input and passes it to some external tool. Later can be a locally run script or a remote REST API.