# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/20 2:36
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/6/7 1:47

import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from golf_federated.utils.log import loggerhear
from golf_federated.utils.query import merge_field_content, merge_field_or_content
from golf_federated.database.table import table_init


class GOLF_SQL(object):
    """

    Class for database in GOLF.

    """

    def __init__(
            self,
            user: str,
            password: str,
            database: str,
            host: str,
            port: int
    ) -> None:
        """

        Initialize the database object.

        Args:
            user (str): Username to connect to the database.
            password (str): Password to connect to the database.
            database (str): Database name to connect to.
            host (str): Uniform Resource Locator to connect to the database.
            port (int): Port number to connect to the database.

        """

        # Initialize object properties.
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        # Setting the URL to connect to the database.
        pymysql.install_as_MySQLdb()
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
            self.user, self.password, self.host, self.port, self.database)

        # Set sqlalchemy to automatically track the database.
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        # The raw SQL statement is not displayed when the query is made.
        self.app.config['SQLALCHEMY_ECHO'] = False

        # Disable automatic submission of data processing.
        self.app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

        # Create database.
        self.db = SQLAlchemy(self.app)

        # Create data table.
        table_init(self.database, self.db)

    def table_find(
            self,
            tablename: str,
            fields: list,
            contents: list
    ) -> dict:
        """

        Find content in data table.

        Args:
            tablename (str): Name of the data table being queried.
            fields (list): List of field name being queried.
            contents (list): List of content corresponding to the field being queried

        Returns:
            Dict: A dictionary containing two fields, flag and data.
                    flag (bool): Indicate whether the process was successful.
                    data (list): List of dictionaries that store the fields and values of each result.

        """

        # Judge whether field length corresponds to content length.
        if len(fields) == len(contents):
            # Connect to the database.
            dbhere = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = dbhere.cursor()

            # SQL statement.
            find_sql = "select * from %s where %s" % (
                tablename,
                merge_field_content(
                    field=fields,
                    content=contents,
                    separator='AND'
                )
            )

            # Execute SQL statement
            try:
                cursor.execute(find_sql)
                data = cursor.fetchall()
                flag = True
                loggerhear.log("Common Info  ", "Find Successful in %s" % tablename)
            except:
                loggerhear.log("Error Message", "Can't Find %s - %s in %s" % (fields, contents, tablename))
                flag = False
                data = 'Error'

            # Close the connection to the database
            dbhere.close()

        else:
            flag = False
            data = 'Error'
            loggerhear.log("Error Message", "Can't Match %s - %s" % (fields, contents))

        return_dict = {'flag': flag, 'data': data}
        return return_dict

    def table_match(
            self,
            tablename: str,
            query_fields: list,
            query_contents: list,
            match_fields: list,
            match_contents: list
    ) -> bool:
        """

        Match content in data table.

        Args:
            tablename (str): Name of the data table being queried.
            query_fields (list): List of field name being queried.
            query_contents: List of content corresponding to the field being queried.
            match_fields: List of field name being matched.
            match_contents: List of content corresponding to the field being matched.

        Returns:
            Bool: Indicate whether the process was successful.

        """

        # Judge whether field length corresponds to content length.
        if len(match_fields) == len(match_contents):
            # Query results of match conditions.
            find_result = self.table_find(tablename=tablename, fields=query_fields, contents=query_contents)
            flag = find_result['flag']
            find_data = find_result['data']

            # Judge whether the query is successful
            if flag:
                # Check if a match is the same as the query result.
                for item in range(len(match_fields)):
                    if find_data[0][match_fields[item]] == match_contents[item]:
                        continue

                    else:
                        flag = False
                        loggerhear.log("Error Message",
                                       "Can't Match %s - %s in %s" % (match_fields, match_contents, tablename))
                        break
                loggerhear.log("Common Info  ", "Match Successful in %s" % tablename)

            else:
                loggerhear.log("Error Message",
                               "Query Contents Not Found (%s - %s) in %s" % (query_fields, query_contents, tablename))

        else:
            flag = False
            loggerhear.log("Error Message", "Can't Match %s - %s" % (match_fields, match_contents))

        return flag

    def table_insert(
            self,
            tablename: str,
            fields: list,
            contents: list
    ) -> bool:
        """

        Insert content in data table.

        Args:
            tablename (str): Name of the data table being queried.
            fields: List of field name being queried.
            contents: List of content corresponding to the field being queried.

        Returns:
            Bool: Indicate whether the process was successful.

        """

        # Judge whether field length corresponds to content length.
        if len(fields) == len(contents):
            # Connect to the database.
            dbhere = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = dbhere.cursor()

            # SQL statement.
            insert_sql = "insert into %s( %s ) values( %s )" % (
                tablename,
                merge_field_or_content(list=fields, separator=',', content=False),
                merge_field_or_content(list=contents, separator=',', content=True)
            )

            # Execute SQL statement
            try:
                cursor.execute(insert_sql)
                dbhere.commit()
                flag = True
                loggerhear.log("Common Info  ", "Insert Successful in %s" % tablename)
            except:
                loggerhear.log("Error Message", "Can't Insert (%s - %s) in %s" % (fields, contents, tablename))
                # raise
                flag = False

            # Close the connection to the database
            dbhere.close()

        else:
            flag = False
            loggerhear.log("Error Message", "Can't Match %s - %s" % (fields, contents))

        return flag

    def table_update(
            self,
            tablename: str,
            query_fields: list,
            query_contents: list,
            update_fields: list,
            update_contents: list
    ) -> bool:
        """

        Update content in data table.

        Args:
            tablename (str): Name of the data table being queried.
            query_fields: List of field name being queried.
            query_contents: List of content corresponding to the field being queried.
            update_fields: List of field name being updated.
            update_contents: List of content corresponding to the field being updated.

        Returns:
            Bool: Indicate whether the process was successful.

        """

        # Judge whether field length corresponds to content length.
        if len(query_fields) == len(query_contents):
            # Judge whether field length corresponds to content length.
            if len(update_fields) == len(update_contents):
                # Connect to the database.
                dbhere = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    cursorclass=pymysql.cursors.DictCursor
                )
                cursor = dbhere.cursor()

                # SQL statement.
                update_sql = "update %s set %s where %s" % (
                    tablename,
                    merge_field_content(field=update_fields, content=update_contents, separator=','),
                    merge_field_content(field=query_fields, content=query_contents, separator='AND')
                )

                # Execute SQL statement
                try:
                    cursor.execute(update_sql)
                    dbhere.commit()
                    flag = True
                    loggerhear.log("Common Info  ", "Update Successful in %s" % tablename)
                except:
                    dbhere.rollback()
                    flag = False
                    loggerhear.log("Error Message",
                                   "Can't Update %s to %s in %s" % (query_contents, update_contents, tablename))

                # Close the connection to the database
                dbhere.close()

            else:
                flag = False
                loggerhear.log("Error Message", "Can't Match %s - %s" % (update_fields, update_contents))

        else:
            flag = False
            loggerhear.log("Error Message", "Can't Match %s - %s" % (query_fields, query_contents))

        return flag

    def table_delete(
            self,
            tablename: str,
            fields: list,
            contents: list
    ) -> dict:
        """

        Delete content in data table.

        Args:
            tablename (str): Name of the data table being queried.
            fields: List of field name being queried.
            contents: List of content corresponding to the field being queried.

        Returns:
            Dict: A dictionary containing two fields, flag and data.
                    flag (bool): Indicate whether the process was successful.
                    data (list): List of dictionaries that store the fields and values of each result.


        """

        # Judge whether field length corresponds to content length.
        if len(fields) == len(contents):
            # Connect to the database.
            dbhere = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = dbhere.cursor()

            # SQL statement.
            find_sql = "delete from %s where %s" % (
                tablename,
                merge_field_content(field=fields, content=contents, separator='AND')
            )

            # Execute SQL statement
            try:
                cursor.execute(find_sql)
                data = cursor.fetchall()
                flag = True
                loggerhear.log("Common Info  ", "Delete Successful in %s" % tablename)
            except:
                loggerhear.log("Error Message",
                               "Can't Delete Contents in %s where %s - %s" % (tablename, fields, contents))
                flag = False
                data = 'Error'

            # Close the connection to the database
            dbhere.close()

        else:
            flag = False
            data = 'Error'
            loggerhear.log("Error Message", "Can't Match %s - %s" % (fields, contents))

        return_dict = {'flag': flag, 'data': data}
        return return_dict

    def table_get(
            self,
            tablename: str
    ) -> dict:
        """

        Get all content in data table.

        Args:
            tablename (str): Name of the data table being queried.

        Returns:
            Dict: A dictionary containing two fields, flag and data.
                    flag (bool): Indicate whether the process was successful.
                    data (list): List of dictionaries that store the fields and values of each result.

        """

        # Connect to the database.
        dbhere = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = dbhere.cursor()

        # SQL statement.
        select_sql = "select * from %s " % (tablename)

        # Execute SQL statement
        try:
            cursor.execute(select_sql)
            data = cursor.fetchall()
            loggerhear.log("Common Info  ", "Get Contents in %s Successful" % tablename)
            flag = True
        except:
            flag = False
            data = 'Error'
            loggerhear.log("Error Message",
                           "Can't Get Contents in %s" % (tablename))

        # Close the connection to the database
        dbhere.close()

        return_dict = {'flag': flag, 'data': data}
        return return_dict
    

    # Add a sql api
    # Delete all content in data table.
    def ALL_TABLE_CLEAR():

        # 打开数据库连接
        flag = False
        db = pymysql.connect(host="localhost", user="root", password=Password, database=Database)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

        # 清空UPLOADED_FILE_INFO和CREATED_FILE_INFO的所有内容
        delete_sql1 = "TRUNCATE TABLE UPLOADED_FILE_INFO"
        delete_sql2 = "TRUNCATE TABLE CREATED_FILE_INFO"
        try:
            # 执行sql语句
            cursor.execute(delete_sql1)
            cursor.execute(delete_sql2)
            # 提交到数据库执行
            db.commit()
            # 关闭数据库连接
            flag = True
        except:
            print("数据删除失败,请查检try语句里的代码")
            # raise
            flag = False

        db.close()
        return str(flag)
