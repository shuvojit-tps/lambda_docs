import sys
import logging
import pymysql
import json
import db_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(db_config.rds_host, user=db_config.name,
                           passwd=db_config.password, db=db_config.db_name, connect_timeout=5)
except:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """

    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        conn.commit()
        cur.execute("select `name`, `email` from `user`")
        users = [row for row in cur]
    conn.commit()

    return {
        'statusCode': 200,
        'body': json.dumps({
            'total': len(users),
            'users': users
        })
    }
