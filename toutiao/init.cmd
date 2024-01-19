DELETE /mytoutiaofav
PUT /mytoutiaofav

@REM PUT _cluster/settings
@REM {
@REM   "persistent": {
@REM     "indices.id_field_data.enabled": true
@REM   }
@REM }


PUT mytoutiaofav/_settings
{
"index.mapping.total_fields.limit": 10000
}
