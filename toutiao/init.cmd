DELETE /mytoutiaofav
PUT /mytoutiaofav

PUT /mytoutiaofav_html

@REM PUT _cluster/settings
@REM {
@REM   "persistent": {
@REM     "indices.id_field_data.enabled": true
@REM   }
@REM }


PUT /mytoutiaofav/_settings
{
"index.mapping.total_fields.limit": 10000
}


PUT /mytoutiaofav/_settings
{
  "index": {
    "max_result_window": 100000  # 你需要的最大值
  }
}


put /mytoutiaofav/_mapping
{
  "properties": {
    "md_content": {
      "type": "text"
    }
  }
}