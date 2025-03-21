package trino
import future.keywords.in
import future.keywords.if
import future.keywords.contains

column_resource := input.action.resource.column
table_resource := input.action.resource.table
schema_resource := input.action.resource.schema
catalog_resource := input.action.resource.catalog

groups := ["admins"]
columns := ["address","ship_name"]

is_admin if {
        input.context.identity.groups == groups
}


columnMask := {"expression": "'XXXXXXXX'"} if {
    print("column_masking")
    print(input)
    not is_admin
    column_resource.columnName in columns
}

