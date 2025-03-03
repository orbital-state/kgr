# Language Definitions

Kgr is a declarative IaC DSL, which aims at capturing a big picture when it comes to DevOps activities:

- What resources are provisioned
- What apps are deployed that consume those resources
- Take care and resolve dependencies
- How all of this can be verified
- How to monitor and secure everything (SRE and ops dimension)

Most importantly, kgr tries to keep things as high-level as possible, so it can be both abstract and concrete when it comes to:

- logical checks (asserts)
- planning deployments and recovery

Language follows a simple rule - everything is a **component** that can be declared and verified to have a certain state.

There are two main definitions kinds for components in kgr:

- Application
- Resource

Each component definition:

- has **meta** data of attributes (mostly for filtering)
- **extends** other definitions 
- **expects** input variables and secrets
- **requires** resources, 
- ****
- ****
## Rules

Each 

rules are defined as conjunction of many  boolean function which are AND 


## Recovery

What risks can we avoid or mitigate? Do we have a backup plan?

Possible recovery approaches when managing failed IaC rollouts usually are:

    - revert to previous known working state (undo change nad re-apply)
    - fix forward
    - rollback deployments
    - big-bang recovery by trying to destroy and provision everything again

and so on

    # --- VERSION PLAN & DEPLOYMENT STRATEGY ---
    version_plan:
        upgrade:
            strategy: blue-green # {rolling, blue-green, canary}
            stages:
            - assert: traffic.shift "20%"
            - assert: terraform.apply
            - assert: traffic.shift "100%"
            rollback:
            - action: revert.previous_version
            - assert: terraform.destroy

        rollback:
            conditions:
            - if: any
                failed_asserts: 
                - terraform.apply
                - http.request
            actions:
            - revert.previous_version
            - notify: "Deployment rollback triggered"

        post-deployment:
            validation:
            - assert: http.request
            - assert: db.migration_success
            cleanup:
            - action: remove_temp_files

        # what about API deprecation plan

# Etc

Main ideas:
- all paths are relative to current file
# - all first level keys except name and kind like {meta, extends, pects}.. 
  are merged
- all asserts are strictly ordered, only claims are parallelized
About variables in kgr:
- each variable is looked up in ENV via upper case key map, 
  i.e. foo can be overwritten by ENV var FOO if defined
- all YAML data types are converted to strings, i.e. bool and 
  int will be str

- vars cannot be empty unless marked as 'empty:true', but required:true is equivalent to not_empty?

- `<component> -> <constraint> -> <rule> -> <action>`

 - actions are mostly sequential and imperative in the context of the rules. hence can accumulate state until final result is computed.
 - rules are independent and isolated in a closure as in functional programming.
 - constraints like `satisfies:` are conjunctions of many rules
 - components provide a high level system overview.