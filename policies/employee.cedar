permit(
    principal,
    action == Action::"tools/call",
    resource
)
when {
    principal.properties.claims.roles.contains("employee") &&
    [
        Tool::"list_incidents",
        Tool::"get_incident",
        Tool::"create_incident",
        Tool::"add_incident_comment"
    ].contains(resource)
};
