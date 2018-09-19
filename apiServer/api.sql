url		网址
header 请求头
params get参数
body	 post参数
method 请求方式
verify 证书认证


CREATE TABLE `movie_info` (   `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',   
`url` varchar(200) DEFAULT NULL COMMENT '接口url',
`params` varchar(200) DEFAULT NULL COMMENT 'get参数',
`body` varchar(200) DEFAULT NULL COMMENT 'post参数',
`header` varchar(200) DEFAULT NULL COMMENT '请求头',
`method` varchar(200) DEFAULT NULL COMMENT '请求方式',
`verify` varchar(200) DEFAULT NULL COMMENT '证书认证',
PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=605 DEFAULT CHARSET=utf8mb4 COMMENT='电影信息表';
SHOW VARIABLES WHERE Variable_name LIKE 'character%' OR Variable_name LIKE 'collation%';