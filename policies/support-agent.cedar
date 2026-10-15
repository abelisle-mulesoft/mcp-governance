permit(
    principal,
    action == Action::"tools/call",
    resource
)
when {
    principal.properties.claims.roles.contains("support-agent") &&
    [
        Tool::"list_incidents",
        Tool::"get_incident",
        Tool::"create_incident",
        Tool::"add_incident_comment",
        Tool::"assign_incident",
        Tool::"update_incident"
    ].contains(resource)
};
