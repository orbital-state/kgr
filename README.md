# kgr

*kgr* 🦘(:KanGoRoo:) is an agnostic, declarative and distributed Infrastructure as Code (IaC) manager and DSL.

It is inspired by IaC projects like kubernetes, crossplane, terraform, etc. In fact, *kguru* stands for "kubernetes-guru" even though it is much more abstract and high-level than k8s.


## Design concepts

Each action is a boolean functions that takes params as payload input and passes it to some external tool. Later can be a locally run script or a remote REST API.


## KanGoRoo language

KanGoRoo or `kgr` is a DSL-like language build around YAML with some additional restrictions like specific schema and custom element lookups.

The programming style is declarative. It is written as tree-like structure in YAML documents and can spread over many files. Such YAML documents contain object structures and are simply called **elements**. Once all files are recursively loaded, the structure of the program can be enriched by evaluating cross-references between YAML documents. Such runtime meta-expansion of the code is achieved by evaluating a simple data type called *Reference ID*.

## Reference ID

*Reference ID* is a string that consists of the `<name>@<lookup>`, where `<name>` is a name of the element and `lookup` is a colon separated list of key-value pairs that can match and filter other elements.

Here are some examples:

    ref: "kgr:id:component/web-app@environment=dev:namespace=app"

Above the prefix "kgr:id:" means that this is a lookup query for an ID of one element. Hence, the list key-value pairs must match a unique and single element (not a list).

Here is another example, which will match a list of elements under ".satisfies":

    items: "kgr:list:component/web-app.satisfies@environment=dev:namespace=app"

Such query results in pulling a list of boolean predicates from web-app.satisfies.

## Classes of kgr Elements

One way of thinking about kgr elements are as object structures (as in JSON). However, all elements in kgr must resolve into a predefined fixed data type. Such grouping into data types is very similar to object-oriented programming where one would have classes of object, so that each object is an instance of the specific data type customarily defined by a user/developer.

So data types are stricter than in YAML. But the language is still agnostic in the sense that each *class* has a particular structure which includes description of a certain expected (think, declared) state. 

To satisfy such state of the object, kgr can perform *actions*. All actions have a boolean outcome of success or failure. If the action was successfully performed on the object then such outcome is interpreted as passed action.
