package trino
import future.keywords.contains
import future.keywords.every
import future.keywords.if
import future.keywords.in

default allow = false

default single_resource = false



# ================== admin ==================

allow if {
    print(input)
    input.context.identity.groups == ["admins"]
}
# access to all batch requests for admin user
single_resource if {
    print(input)
    input.context.identity.groups == ["admins"]
}

# ================== resources access user ==================
allow if {
        print(input)
        input.action.operation == "AccessCatalog"
        input.action.resource.catalog.name == "datahub_test"
        "human" = input.context.identity.groups[_]
    }

allow if {
        print(input)
        input.action.operation == "ShowSchemas"
        input.action.resource.catalog.name == "datahub_test"
        "human" = input.context.identity.groups[_]
}

allow if {
        print(input)
        input.action.operation == "ShowTables"
        input.action.resource.schema.catalogName == "datahub_test"
        "human" = input.context.identity.groups[_]
}

allow if {
        print(input)
        input.action.operation == "ShowColumns"
        input.action.resource.schema.catalogName == "datahub_test"
        "human" = input.context.identity.groups[_]
}

allow if {
        print(input)
        input.action.operation == "SelectFromColumns"
        input.action.resource.table.catalogName == "datahub_test"
        "human" = input.context.identity.groups[_]
}

allow if {
        input.action.operation == "ExecuteQuery"
        "human" = input.context.identity.groups[_]
}




# ================== batch ==================
 
# ... rest of the policy ...
# this assumes the non-batch response field is called "allow"
batch contains i if {
    some i
    raw_resource := input.action.filterResources[i]
    single_resource with input.action.resource as raw_resource
}
 
# Corner case: filtering columns is done with a single table item, and many columns inside
# We cannot use our normal logic in other parts of the policy as they are based on sets
# and we need to retain order
batch contains i if {
    some i
    input.action.operation == "FilterColumns"
    count(input.action.filterResources) == 1
    raw_resource := input.action.filterResources[0]
    count(raw_resource["table"]["columns"]) > 0
    new_resources := [
        object.union(raw_resource, {"table": {"column": column_name}})
        | column_name := raw_resource["table"]["columns"][_]
    ]
    single_resource with input.action.resource as new_resources[i]
}
